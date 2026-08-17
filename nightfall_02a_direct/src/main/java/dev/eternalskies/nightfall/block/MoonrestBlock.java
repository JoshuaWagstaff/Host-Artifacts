package dev.eternalskies.nightfall.block;

import dev.eternalskies.nightfall.event.DuskblightManager;
import net.minecraft.ChatFormatting;
import net.minecraft.core.BlockPos;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.shapes.CollisionContext;
import net.minecraft.world.phys.shapes.Shapes;
import net.minecraft.world.phys.shapes.VoxelShape;

/** Duskborn reverse-rest shrine: calls dusk without behaving like a normal bed. */
public class MoonrestBlock extends Block {
    private static final long DUSK = 13_000L;
    private static final long NIGHT_END = 23_000L;
    private static final long DAY = 24_000L;

    private static final VoxelShape SHAPE = Shapes.or(
        Block.box(0.5D, 0.0D, 1.0D, 15.5D, 4.5D, 15.0D),
        Block.box(1.2D, 4.5D, 11.0D, 14.8D, 8.0D, 14.5D),
        Block.box(0.0D, 4.0D, 12.5D, 2.0D, 9.2D, 15.0D),
        Block.box(14.0D, 4.0D, 12.5D, 16.0D, 9.2D, 15.0D)
    );

    public MoonrestBlock(Properties properties) {
        super(properties);
    }

    @Override
    public VoxelShape getShape(BlockState state, BlockGetter level, BlockPos pos, CollisionContext context) {
        return SHAPE;
    }

    @Override
    public InteractionResult use(BlockState state, Level level, BlockPos pos,
                                 Player player, InteractionHand hand, BlockHitResult hit) {
        if (level.isClientSide) return InteractionResult.SUCCESS;
        if (!(level instanceof ServerLevel serverLevel) || !(player instanceof ServerPlayer serverPlayer)) {
            return InteractionResult.PASS;
        }

        if (!DuskblightManager.isVampire(serverPlayer)) {
            serverPlayer.displayClientMessage(Component.literal("Moonrest answers only the Duskborn.")
                .withStyle(ChatFormatting.DARK_PURPLE), true);
            return InteractionResult.CONSUME;
        }

        long absolute = serverLevel.getDayTime();
        long clock = Math.floorMod(absolute, DAY);
        if (clock >= DUSK && clock <= NIGHT_END) {
            serverPlayer.displayClientMessage(Component.literal("Moonrest is quiet beneath the night. The Dusk Altar is where deeper powers awaken.")
                .withStyle(ChatFormatting.GRAY), true);
            return InteractionResult.CONSUME;
        }

        boolean daylightWalkerPresent = serverLevel.players().stream()
            .filter(p -> !p.isSpectator())
            .anyMatch(p -> !DuskblightManager.isVampire(p));
        if (daylightWalkerPresent) {
            serverPlayer.displayClientMessage(Component.literal("The dusk cannot be called while daylight walkers remain awake here.")
                .withStyle(ChatFormatting.GRAY), true);
            return InteractionResult.CONSUME;
        }

        long startOfDay = absolute - clock;
        long target = startOfDay + DUSK;
        if (clock > NIGHT_END) target += DAY;
        serverLevel.setDayTime(target);

        serverPlayer.sendSystemMessage(Component.literal("You surrender the daylight. Dusk settles over the sky.")
            .withStyle(ChatFormatting.DARK_PURPLE));
        return InteractionResult.CONSUME;
    }
}
