package dev.eternalskies.nightfall.client;

import dev.eternalskies.nightfall.EternalSkiesNightfall;
import dev.eternalskies.nightfall.event.DuskPowerManager;
import dev.eternalskies.nightfall.registry.NightfallEntities;
import net.minecraft.client.renderer.item.ItemProperties;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.Item;
import net.minecraftforge.api.distmarker.Dist;
import net.minecraftforge.client.event.EntityRenderersEvent;
import net.minecraftforge.client.event.RegisterGuiOverlaysEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.event.lifecycle.FMLClientSetupEvent;
import net.minecraftforge.registries.ForgeRegistries;

@Mod.EventBusSubscriber(modid = EternalSkiesNightfall.MOD_ID, bus = Mod.EventBusSubscriber.Bus.MOD, value = Dist.CLIENT)
public final class NightfallClientEvents {
    private NightfallClientEvents() {}

    @SubscribeEvent
    public static void clientSetup(FMLClientSetupEvent event) {
        // Preserve the native Aether Vampire Blade model until the actual blade
        // has been Eclipse-bound, then switch only that NBT-tagged stack to the
        // ornate Nightfall relic model.
        event.enqueueWork(() -> {
            Item vampireBlade = ForgeRegistries.ITEMS.getValue(new ResourceLocation("aether", "vampire_blade"));
            if (vampireBlade != null) {
                ItemProperties.register(vampireBlade,
                    new ResourceLocation(EternalSkiesNightfall.MOD_ID, "duskbound"),
                    (stack, level, entity, seed) -> DuskPowerManager.isDuskboundVampireBlade(stack) ? 1.0F : 0.0F);
            }
        });
    }

    @SubscribeEvent
    public static void registerHud(RegisterGuiOverlaysEvent event) {
        event.registerAboveAll("dusk_status", DuskHudOverlay.HUD);
    }

    @SubscribeEvent
    public static void registerLayerDefinitions(EntityRenderersEvent.RegisterLayerDefinitions event) {
        event.registerLayerDefinition(DuskbornModel.LAYER, DuskbornModel::createBodyLayer);
    }

    @SubscribeEvent
    public static void registerRenderers(EntityRenderersEvent.RegisterRenderers event) {
        event.registerEntityRenderer(NightfallEntities.DUSKBORN.get(), DuskbornRenderer::new);
    }
}
