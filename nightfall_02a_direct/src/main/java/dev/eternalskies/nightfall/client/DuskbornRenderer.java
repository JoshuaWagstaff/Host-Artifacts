package dev.eternalskies.nightfall.client;

import dev.eternalskies.nightfall.EternalSkiesNightfall;
import dev.eternalskies.nightfall.entity.DuskbornEntity;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.renderer.entity.HumanoidMobRenderer;
import net.minecraft.resources.ResourceLocation;

public final class DuskbornRenderer extends HumanoidMobRenderer<DuskbornEntity, DuskbornModel> {
    private static final ResourceLocation TEXTURE =
        new ResourceLocation(EternalSkiesNightfall.MOD_ID, "textures/entity/duskborn.png");

    public DuskbornRenderer(EntityRendererProvider.Context context) {
        super(context, new DuskbornModel(context.bakeLayer(DuskbornModel.LAYER)), 0.50F);
        this.addLayer(new DuskbornGlowLayer(this));
    }

    @Override
    public ResourceLocation getTextureLocation(DuskbornEntity entity) {
        return TEXTURE;
    }
}
