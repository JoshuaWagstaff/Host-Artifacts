package dev.eternalskies.nightfall.client;

import dev.eternalskies.nightfall.EternalSkiesNightfall;
import dev.eternalskies.nightfall.entity.DuskbornEntity;
import net.minecraft.client.model.HumanoidModel;
import net.minecraft.client.model.ZombieModel;
import net.minecraft.client.model.geom.ModelLayerLocation;
import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeDeformation;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.util.Mth;

/**
 * Nightfall art-pass Duskborn model.
 *
 * The vanilla humanoid skeleton is intentionally retained so melee/locomotion
 * reads correctly beside Aether mobs, but the silhouette is rebuilt with a
 * fitted nightblade coat, raised collar, celestial shoulder armor, chain and
 * pendant, split coat tails, and a broken spectral-feather mantle. Nothing in
 * this model is intended to read as a bat wing or a default zombie reskin.
 */
public final class DuskbornModel extends ZombieModel<DuskbornEntity> {
    public static final ModelLayerLocation LAYER = new ModelLayerLocation(
        new ResourceLocation(EternalSkiesNightfall.MOD_ID, "duskborn"), "main");

    private final ModelPart leftMantle;
    private final ModelPart rightMantle;
    private final ModelPart leftTail;
    private final ModelPart rightTail;
    private final ModelPart centerTail;
    private final ModelPart pendant;

    public DuskbornModel(ModelPart root) {
        super(root);
        this.leftMantle = this.body.getChild("left_mantle");
        this.rightMantle = this.body.getChild("right_mantle");
        this.leftTail = this.body.getChild("left_tail");
        this.rightTail = this.body.getChild("right_tail");
        this.centerTail = this.body.getChild("center_tail");
        this.pendant = this.body.getChild("pendant");
    }

    public static LayerDefinition createBodyLayer() {
        MeshDefinition mesh = HumanoidModel.createMesh(CubeDeformation.NONE, 0.0F);
        PartDefinition root = mesh.getRoot();
        PartDefinition body = root.getChild("body");

        body.addOrReplaceChild("nightblade_coat",
            CubeListBuilder.create()
                .texOffs(64, 0).addBox(-4.0F, 0.0F, -2.0F, 8.0F, 8.0F, 4.0F,
                    new CubeDeformation(0.18F)),
            PartPose.ZERO);

        body.addOrReplaceChild("left_collar",
            CubeListBuilder.create().texOffs(96, 0)
                .addBox(-4.55F, -1.25F, -1.45F, 1.7F, 4.1F, 3.0F, new CubeDeformation(0.08F)),
            PartPose.rotation(0.0F, 0.0F, -0.16F));
        body.addOrReplaceChild("right_collar",
            CubeListBuilder.create().texOffs(106, 0)
                .addBox(2.85F, -1.25F, -1.45F, 1.7F, 4.1F, 3.0F, new CubeDeformation(0.08F)),
            PartPose.rotation(0.0F, 0.0F, 0.16F));
        body.addOrReplaceChild("back_collar",
            CubeListBuilder.create().texOffs(116, 0)
                .addBox(-3.0F, -1.55F, 1.45F, 6.0F, 3.1F, 1.25F, CubeDeformation.NONE),
            PartPose.rotation(-0.08F, 0.0F, 0.0F));

        body.addOrReplaceChild("left_shoulderguard",
            CubeListBuilder.create().texOffs(64, 24)
                .addBox(-6.0F, -0.85F, -2.35F, 3.2F, 2.4F, 4.7F, new CubeDeformation(0.12F)),
            PartPose.rotation(0.0F, 0.0F, -0.08F));
        body.addOrReplaceChild("right_shoulderguard",
            CubeListBuilder.create().texOffs(80, 24)
                .addBox(2.8F, -0.85F, -2.35F, 3.2F, 2.4F, 4.7F, new CubeDeformation(0.12F)),
            PartPose.rotation(0.0F, 0.0F, 0.08F));

        body.addOrReplaceChild("chain_left",
            CubeListBuilder.create().texOffs(96, 20)
                .addBox(-2.25F, 1.0F, -2.30F, 0.55F, 4.1F, 0.45F, CubeDeformation.NONE),
            PartPose.rotation(0.0F, 0.0F, -0.25F));
        body.addOrReplaceChild("chain_right",
            CubeListBuilder.create().texOffs(100, 20)
                .addBox(1.70F, 1.0F, -2.30F, 0.55F, 4.1F, 0.45F, CubeDeformation.NONE),
            PartPose.rotation(0.0F, 0.0F, 0.25F));
        body.addOrReplaceChild("pendant",
            CubeListBuilder.create().texOffs(104, 20)
                .addBox(-0.75F, 4.1F, -2.60F, 1.5F, 1.7F, 0.65F, new CubeDeformation(0.03F)),
            PartPose.ZERO);

        body.addOrReplaceChild("belt",
            CubeListBuilder.create().texOffs(64, 36)
                .addBox(-4.25F, 7.05F, -2.18F, 8.5F, 1.3F, 4.35F, new CubeDeformation(0.04F)),
            PartPose.ZERO);

        PartDefinition leftTail = body.addOrReplaceChild("left_tail",
            CubeListBuilder.create().texOffs(64, 44)
                .addBox(-3.65F, 0.0F, -0.55F, 3.0F, 9.5F, 1.0F, CubeDeformation.NONE),
            PartPose.offsetAndRotation(0.0F, 7.8F, 2.0F, 0.10F, 0.03F, -0.05F));
        leftTail.addOrReplaceChild("left_tail_tip",
            CubeListBuilder.create().texOffs(74, 44)
                .addBox(-2.8F, -0.2F, -0.48F, 2.2F, 5.0F, 0.9F, CubeDeformation.NONE),
            PartPose.offsetAndRotation(-0.25F, 8.1F, 0.0F, 0.08F, 0.0F, 0.11F));

        PartDefinition rightTail = body.addOrReplaceChild("right_tail",
            CubeListBuilder.create().texOffs(82, 44)
                .addBox(0.65F, 0.0F, -0.55F, 3.0F, 8.0F, 1.0F, CubeDeformation.NONE),
            PartPose.offsetAndRotation(0.0F, 7.8F, 2.0F, 0.12F, -0.02F, 0.06F));
        rightTail.addOrReplaceChild("right_tail_tip",
            CubeListBuilder.create().texOffs(92, 44)
                .addBox(0.60F, -0.2F, -0.48F, 2.1F, 4.2F, 0.9F, CubeDeformation.NONE),
            PartPose.offsetAndRotation(0.30F, 6.9F, 0.0F, 0.09F, 0.0F, -0.13F));

        body.addOrReplaceChild("center_tail",
            CubeListBuilder.create().texOffs(101, 44)
                .addBox(-1.25F, 0.0F, -0.45F, 2.5F, 6.4F, 0.8F, CubeDeformation.NONE),
            PartPose.offsetAndRotation(0.0F, 8.0F, 2.18F, 0.16F, 0.0F, 0.0F));

        PartDefinition leftMantle = body.addOrReplaceChild("left_mantle",
            CubeListBuilder.create().texOffs(64, 64)
                .addBox(0.0F, -0.7F, -0.42F, 2.2F, 7.4F, 0.8F, CubeDeformation.NONE),
            PartPose.offsetAndRotation(3.0F, 0.7F, 2.15F, 0.12F, 0.24F, -0.45F));
        leftMantle.addOrReplaceChild("left_shard_a",
            CubeListBuilder.create().texOffs(74, 64)
                .addBox(0.0F, 0.0F, -0.36F, 2.0F, 8.0F, 0.7F, CubeDeformation.NONE),
            PartPose.offsetAndRotation(1.15F, 4.6F, 0.0F, 0.03F, 0.03F, -0.30F));
        leftMantle.addOrReplaceChild("left_shard_b",
            CubeListBuilder.create().texOffs(84, 64)
                .addBox(0.0F, 0.0F, -0.32F, 1.7F, 6.2F, 0.65F, CubeDeformation.NONE),
            PartPose.offsetAndRotation(-0.10F, 5.9F, 0.1F, 0.02F, -0.06F, 0.16F));
        leftMantle.addOrReplaceChild("left_shard_c",
            CubeListBuilder.create().texOffs(92, 64)
                .addBox(0.0F, 0.0F, -0.30F, 1.4F, 4.7F, 0.6F, CubeDeformation.NONE),
            PartPose.offsetAndRotation(2.2F, 2.7F, 0.0F, -0.02F, 0.08F, -0.50F));

        PartDefinition rightMantle = body.addOrReplaceChild("right_mantle",
            CubeListBuilder.create().texOffs(100, 64)
                .addBox(-2.2F, -0.7F, -0.42F, 2.2F, 6.3F, 0.8F, CubeDeformation.NONE),
            PartPose.offsetAndRotation(-3.0F, 1.0F, 2.15F, 0.10F, -0.22F, 0.49F));
        rightMantle.addOrReplaceChild("right_shard_a",
            CubeListBuilder.create().texOffs(110, 64)
                .addBox(-2.0F, 0.0F, -0.36F, 2.0F, 6.5F, 0.7F, CubeDeformation.NONE),
            PartPose.offsetAndRotation(-1.10F, 3.9F, 0.0F, 0.02F, -0.02F, 0.33F));
        rightMantle.addOrReplaceChild("right_shard_b",
            CubeListBuilder.create().texOffs(120, 64)
                .addBox(-1.45F, 0.0F, -0.30F, 1.45F, 4.4F, 0.6F, CubeDeformation.NONE),
            PartPose.offsetAndRotation(0.0F, 4.7F, 0.1F, 0.03F, 0.08F, -0.20F));

        return LayerDefinition.create(mesh, 128, 128);
    }

    @Override
    public void setupAnim(DuskbornEntity entity, float limbSwing, float limbSwingAmount,
                          float ageInTicks, float netHeadYaw, float headPitch) {
        super.setupAnim(entity, limbSwing, limbSwingAmount, ageInTicks, netHeadYaw, headPitch);

        float breath = Mth.sin(ageInTicks * 0.085F) * 0.045F;
        float cloth = Mth.sin(ageInTicks * 0.055F + 1.2F) * 0.035F;
        float aggressive = entity.getTarget() != null ? 0.13F : 0.0F;

        this.leftMantle.zRot = -0.45F - breath - aggressive;
        this.rightMantle.zRot = 0.49F + breath + aggressive * 0.85F;
        this.leftMantle.yRot = 0.24F + breath * 0.45F;
        this.rightMantle.yRot = -0.22F - breath * 0.45F;

        this.leftTail.xRot = 0.10F + cloth + limbSwingAmount * 0.10F;
        this.rightTail.xRot = 0.12F - cloth + limbSwingAmount * 0.08F;
        this.centerTail.xRot = 0.16F + breath * 0.4F;
        this.pendant.zRot = breath * 0.35F;
    }
}
