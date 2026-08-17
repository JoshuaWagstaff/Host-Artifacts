#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from pathlib import Path
root=Path('nightfall_reboot/src/main/java/dev/eternalskies/nightfall/entity')
for name in ['DuskbornEntity.java','StormlingEntity.java']:
    p=root/name
    s=p.read_text()
    s=s.replace('import net.minecraft.world.entity.ai.goal.target.HurtByTargetGoal;\n','')
    if name == 'DuskbornEntity.java':
        s=s.replace('        this.targetSelector.addGoal(1, new HurtByTargetGoal(this).setAlertOthers(DuskbornEntity.class));\n','')
        s=s.replace('        this.targetSelector.addGoal(2, new NearestAttackableTargetGoal<>(this, Player.class, true));\n','        this.targetSelector.addGoal(1, new NearestAttackableTargetGoal<>(this, Player.class, true));\n')
    else:
        s=s.replace('        this.targetSelector.addGoal(1, new HurtByTargetGoal(this));\n','')
        s=s.replace('        this.targetSelector.addGoal(2, new NearestAttackableTargetGoal<>(this, Player.class, true));\n','        this.targetSelector.addGoal(1, new NearestAttackableTargetGoal<>(this, Player.class, true));\n')
    p.write_text(s)
PY
