package dev.eternalskies.nightfall.world;

import com.mojang.serialization.Codec;
import dev.eternalskies.nightfall.registry.NightfallBlocks;
import dev.eternalskies.nightfall.registry.NightfallEntities;
import dev.eternalskies.nightfall.entity.DuskbornEntity;
import net.minecraft.core.BlockPos;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.util.RandomSource;
import net.minecraft.world.level.WorldGenLevel;
import net.minecraft.world.entity.MobSpawnType;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.level.levelgen.feature.Feature;
import net.minecraft.world.level.levelgen.feature.FeaturePlaceContext;
import net.minecraft.world.level.levelgen.feature.configurations.NoneFeatureConfiguration;
import net.minecraftforge.registries.ForgeRegistries;

/**
 * A rare ruined celestial shelter that has fallen into dusk.
 *
 * Design constraints:
 * - unmistakably Aether-native: Holystone, moss, Skyroot, no gothic blackstone castle
 * - roofed/shaded interior so the ruin itself explains how light-intolerant Duskborn survive daytime
 * - a Dusk Altar at the heart, teaching the player that dusk communion predates them
 * - intentionally small; this is an atmospheric landmark, not a dungeon replacement
 */
public final class DuskRefugeFeature extends Feature<NoneFeatureConfiguration> {
    private static final ResourceLocation HOLYSTONE = new ResourceLocation("aether", "holystone");
    private static final ResourceLocation MOSSY_HOLYSTONE = new ResourceLocation("aether", "mossy_holystone");
    private static final ResourceLocation HOLYSTONE_BRICKS = new ResourceLocation("aether", "holystone_bricks");
    private static final ResourceLocation SKYROOT_PLANKS = new ResourceLocation("aether", "skyroot_planks");

    public DuskRefugeFeature(Codec<NoneFeatureConfiguration> codec) {
        super(codec);
    }

    @Override
    public boolean place(FeaturePlaceContext<NoneFeatureConfiguration> context) {
        WorldGenLevel level = context.level();
        BlockPos origin = context.origin();
        RandomSource random = context.random();

        // The biome modifier targets the Aether tag, but keep a defensive dimension check.
        if (!"aether:the_aether".equals(level.getLevel().dimension().location().toString())) return false;

        Block holystone = block(HOLYSTONE);
        Block mossy = block(MOSSY_HOLYSTONE);
        Block bricks = block(HOLYSTONE_BRICKS);
        Block skyroot = block(SKYROOT_PLANKS);
        if (holystone == null || mossy == null || bricks == null || skyroot == null) return false;

        // Normalize onto the local surface ourselves instead of trusting the incoming Y.
        // This is important for /place feature (which bypasses placed-feature heightmap
        // modifiers) and also makes natural generation resilient to ordinary Aether slopes.
        int centerY = surfaceY(level, origin.getX(), origin.getZ());
        BlockPos center = new BlockPos(origin.getX(), centerY, origin.getZ());
        BlockPos centerSupport = center.below();
        if (level.isEmptyBlock(centerSupport) || !level.getFluidState(centerSupport).isEmpty()) return false;

        // Refuse only genuinely tiny ledges/cliffs. Aether islands are rolling terrain, so
        // demanding all support points at exactly the same Y made the old refuge reject
        // most valid sites. Up to four blocks of relief is safe because the foundation
        // below is filled down into the terrain.
        int[][] tests = {
            {0,0},{4,0},{-4,0},{0,4},{0,-4},
            {4,4},{4,-4},{-4,4},{-4,-4}
        };
        for (int[] t : tests) {
            int sampleY = surfaceY(level, center.getX() + t[0], center.getZ() + t[1]);
            BlockPos support = new BlockPos(center.getX() + t[0], sampleY - 1, center.getZ() + t[1]);
            if (level.isEmptyBlock(support) || !level.getFluidState(support).isEmpty()) return false;
            if (Math.abs(sampleY - centerY) > 4) return false;
        }

        // 11x11 broken foundation. The interior is deliberately recessed and mostly roofed.
        for (int dx = -5; dx <= 5; dx++) {
            for (int dz = -5; dz <= 5; dz++) {
                boolean cornerCut = Math.abs(dx) == 5 && Math.abs(dz) == 5;
                if (cornerCut) continue;
                BlockState floor = random.nextFloat() < 0.24F
                    ? mossy.defaultBlockState()
                    : bricks.defaultBlockState();

                BlockPos floorPos = center.offset(dx, -1, dz);
                int localSurfaceY = surfaceY(level, floorPos.getX(), floorPos.getZ());
                set(level, floorPos, floor);

                // If the local island surface drops below the chosen floor, extend a short
                // ruined foundation downward so the refuge hugs the island instead of
                // floating over small dips.
                int lowestFillY = Math.max(localSurfaceY - 1, floorPos.getY() - 4);
                for (int y = floorPos.getY() - 1; y >= lowestFillY; y--) {
                    BlockPos fill = new BlockPos(floorPos.getX(), y, floorPos.getZ());
                    if (!level.isEmptyBlock(fill)) break;
                    set(level, fill, (random.nextFloat() < 0.20F ? mossy : holystone).defaultBlockState());
                }

                // Clear enough space to stop vegetation/terrain from filling the refuge.
                for (int dy = 0; dy <= 4; dy++) {
                    BlockPos clear = center.offset(dx, dy, dz);
                    if (!level.getBlockState(clear).is(Blocks.BEDROCK)) set(level, clear, Blocks.AIR.defaultBlockState());
                }
            }
        }

        // Low ruined perimeter with deliberate breaches on each side.
        for (int y = 0; y <= 2; y++) {
            for (int d = -4; d <= 4; d++) {
                if (Math.abs(d) <= 1) continue; // cardinal door/breach openings
                placeWall(level, center.offset(d, y, -5), random, bricks, mossy);
                placeWall(level, center.offset(d, y, 5), random, bricks, mossy);
                placeWall(level, center.offset(-5, y, d), random, bricks, mossy);
                placeWall(level, center.offset(5, y, d), random, bricks, mossy);
            }
        }

        // Four surviving pillars make the silhouette read as a celestial ruin from a distance.
        int[][] pillars = {{-4,-4},{4,-4},{-4,4},{4,4}};
        for (int[] p : pillars) {
            int height = 3 + random.nextInt(2);
            for (int y = 0; y <= height; y++) {
                set(level, center.offset(p[0], y, p[1]),
                    (random.nextFloat() < 0.18F ? mossy : bricks).defaultBlockState());
            }
        }

        // A compact roof creates the daylight-safe heart of the refuge.
        // Skyroot beams keep it recognizably Aether rather than a generic stone crypt.
        for (int dx = -3; dx <= 3; dx++) {
            for (int dz = -3; dz <= 3; dz++) {
                if ((Math.abs(dx) == 3 && Math.abs(dz) == 3) || random.nextFloat() < 0.08F) continue;
                BlockState roof = (dx == 0 || dz == 0)
                    ? skyroot.defaultBlockState()
                    : (random.nextFloat() < 0.16F ? mossy : bricks).defaultBlockState();
                set(level, center.offset(dx, 4, dz), roof);
            }
        }

        // Central dais and altar. Players can find or craft the altar; the structure does not gate progression.
        for (int dx = -1; dx <= 1; dx++) {
            for (int dz = -1; dz <= 1; dz++) {
                set(level, center.offset(dx, 0, dz), holystone.defaultBlockState());
            }
        }
        set(level, center.above(), NightfallBlocks.DUSK_ALTAR.get().defaultBlockState());

        // Four low offering stones teach the altar language without a GUI or lore book.
        // Dropped ritual items can be laid on/around these stones and remain visibly
        // present during communion. The altar still works when player-crafted elsewhere.
        int[][] offeringStones = {{-2,0},{2,0},{0,-2},{0,2}};
        for (int[] p : offeringStones) {
            set(level, center.offset(p[0], 0, p[1]), holystone.defaultBlockState());
        }

        // Small broken Skyroot benches suggest this was once a place of contemplation, not a vampire fortress.
        for (int dz : new int[]{-2, 2}) {
            set(level, center.offset(-2, 0, dz), skyroot.defaultBlockState());
            set(level, center.offset(2, 0, dz), skyroot.defaultBlockState());
        }

        // One resident makes discovery meaningful without turning the refuge into an infinite mob farm.
        spawnResident(level, center.offset(0, 1, 2));
        if (random.nextFloat() < 0.35F) spawnResident(level, center.offset(2, 1, -1));

        return true;
    }

    private static void spawnResident(WorldGenLevel level, BlockPos pos) {
        DuskbornEntity duskborn = NightfallEntities.DUSKBORN.get().create(level.getLevel());
        if (duskborn == null) return;
        duskborn.moveTo(pos.getX() + 0.5D, pos.getY(), pos.getZ() + 0.5D, level.getRandom().nextFloat() * 360.0F, 0.0F);
        duskborn.finalizeSpawn(level, level.getCurrentDifficultyAt(pos), MobSpawnType.STRUCTURE, null, null);
        duskborn.setPersistenceRequired();
        level.addFreshEntity(duskborn);
    }

    private static int surfaceY(WorldGenLevel level, int x, int z) {
        return level.getHeight(Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, x, z);
    }

    private static void placeWall(WorldGenLevel level, BlockPos pos, RandomSource random, Block bricks, Block mossy) {
        // More missing upper blocks makes it a ruin rather than a sealed box.
        if (pos.getY() > level.getMinBuildHeight() && random.nextFloat() < 0.16F) return;
        set(level, pos, (random.nextFloat() < 0.28F ? mossy : bricks).defaultBlockState());
    }

    private static Block block(ResourceLocation id) {
        Block block = ForgeRegistries.BLOCKS.getValue(id);
        return block == Blocks.AIR ? null : block;
    }

    private static void set(WorldGenLevel level, BlockPos pos, BlockState state) {
        level.setBlock(pos, state, 2);
    }
}
