package dev.eternalskies.nightfall.client;

import dev.eternalskies.nightfall.EternalSkiesNightfall;
import dev.eternalskies.nightfall.entity.DuskbornEntity;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.client.renderer.entity.layers.EyesLayer;
import net.minecraft.client.renderer.entity.RenderLayerParent;
import net.minecraft.resources.ResourceLocation;

/** Full-bright red eyes plus a restrained pendant/rune ember. */
public final class DuskbornGlowLayer extends EyesLayer<DuskbornEntity, DuskbornModel> {
    private static final RenderType GLOW = RenderType.eyes(new ResourceLocation(
        EternalSkiesNightfall.MOD_ID, "textures/entity/duskborn_glow.png"));

    public DuskbornGlowLayer(RenderLayerParent<DuskbornEntity, DuskbornModel> parent) {
        super(parent);
    }

    @Override
    public RenderType renderType() {
        return GLOW;
    }
}
