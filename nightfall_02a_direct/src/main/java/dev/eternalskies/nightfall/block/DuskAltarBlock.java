package dev.eternalskies.nightfall.block;

import dev.eternalskies.nightfall.event.DuskRitualManager;
import dev.eternalskies.nightfall.event.DuskblightManager;
import net.minecraft.ChatFormatting;
import net.minecraft.core.BlockPos;
import net.minecraft.network.chat.Component;
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

/**
 * Physical communion altar. The 0.2 art pass gives it a low celestial dais,
 * four corner pylons and a central dusk-core recess instead of a cube.
 */
public class DuskAltarBlock extends Block {
    private static final VoxelShape SHAPE = Shapes.or(
        Block.box(0.0D, 0.0D, 0.0D, 16.0D, 6.0D, 16.0D),
        Block.box(1.0D, 6.0D, 1.0D, 4.0D, 11.0D, 4.0D),
        Block.box(12.0D, 6.0D, 1.0D, 15.0D, 11.0D, 4.0D),
        Block.box(1.0D, 6.0D, 12.0D, 4.0D, 11.0D, 15.0D),
        Block.box(12.0D, 6.0D, 12.0D, 15.0D, 11.0D, 15.0D)
    );

    public DuskAltarBlock(Properties properties) {
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
        if (!(player instanceof ServerPlayer serverPlayer)) return InteractionResult.PASS;

        if (!DuskblightManager.isVampire(serverPlayer)) {
            serverPlayer.displayClientMessage(Component.literal("The altar remains cold beneath a daylight soul.")
                .withStyle(ChatFormatting.GRAY), true);
            return InteractionResult.CONSUME;
        }

        return DuskRitualManager.tryBegin(serverPlayer, pos)
            ? InteractionResult.CONSUME
            : InteractionResult.PASS;
    }
}
