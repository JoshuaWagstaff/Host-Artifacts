package dev.eternalskies.nightfall.registry;

import dev.eternalskies.nightfall.EternalSkiesNightfall;
import dev.eternalskies.nightfall.block.MoonrestBlock;
import dev.eternalskies.nightfall.block.DuskAltarBlock;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;
import net.minecraftforge.registries.RegistryObject;

public final class NightfallBlocks {
    private NightfallBlocks() {}

    public static final DeferredRegister<Block> BLOCKS =
        DeferredRegister.create(ForgeRegistries.BLOCKS, EternalSkiesNightfall.MOD_ID);


    public static final RegistryObject<Block> DUSK_ALTAR = BLOCKS.register("dusk_altar",
        () -> new DuskAltarBlock(BlockBehaviour.Properties.of()
            .strength(3.0F, 6.0F)
            .sound(SoundType.STONE)
            .noOcclusion()
            .lightLevel(state -> 4)));

    public static final RegistryObject<Block> MOONREST = BLOCKS.register("moonrest",
        () -> new MoonrestBlock(BlockBehaviour.Properties.of()
            .strength(1.2F)
            .sound(SoundType.WOOL)
            .noOcclusion()));
}
