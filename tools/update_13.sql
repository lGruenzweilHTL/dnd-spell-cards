UPDATE spells SET summary = 'Mental contact with extraplanar entity. {@dc 15} Intelligence save or take {@damage 6d6} psychic damage and gain {@condition insane}} condition. Success: ask entity up to five questions answered one word each.' WHERE slug = 'contact-other-plane';

UPDATE spells SET summary = 'Touch attack inflicts disease. Target {@condition poisoned}}, must save Constitution each turn. Three successes: disease ends. Three failures: choose disease (Blinding Sickness: {@condition blinded}}, disadvantage Wisdom; Filth Fever: disadvantage Strength; Flesh Rot: disadvantage Charisma, vulnerability all damage; Mindfire: disadvantage Intelligence, behaves as {@spell confusion}}; Seizure: disadvantage Dexterity; Slimy Doom: disadvantage Constitution, {@condition stunned}} after damage).' WHERE slug = 'contagion';

UPDATE spells SET summary = 'Create nonliving object from Shadowfell up to 5-foot cube: vegetable matter, mineral, soft goods, or metal you''ve seen. Material created by spell cannot be used as spell component for other spells.' WHERE slug = 'creation';

UPDATE spells SET summary = '30-foot-radius, 40-foot-high cylinder of bright sunlight appears at location. Creatures entering or ending turn in cylinder: {@dc} Constitution save or take {@damage 4d10} radiant damage (half on success). Move cylinder up to 60 feet bonus action if within 60 feet.' WHERE slug = 'dawn';

UPDATE spells SET summary = 'Protective barrier around you. Celestials, elementals, fey, fiends, undead have disadvantage on attacks against you. Break Enchantment: touch creature {@condition charmed}}, {@condition frightened}}, or possessed—remove condition. Dismissal: melee spell attack celestial/elemental/fey/fiend/undead—Charisma save or sent to home plane.' WHERE slug = 'dispel-evil-and-good';

UPDATE spells SET summary = 'Tendril of darkness drains life. Target Dexterity save or take {@damage 2d8} necrotic (success, spell ends) or {@damage 4d8} necrotic (fail, continue each turn as action). You regain HP equal to half damage dealt. Ends if you act otherwise or target leaves range.' WHERE slug = 'enervation';

UPDATE spells SET summary = 'Vertical column of fire and radiance in 10-foot-radius, 40-foot-high cylinder. Creatures: {@dc} Dexterity save or take {@damage 4d6} fire and {@damage 4d6} radiant damage (half on success).' WHERE slug = 'flame-strike';

UPDATE spells SET summary = 'Place magical command on creature forcing action/inaction. {@dc} Wisdom save or become {@condition charmed}}. Target takes {@damage 5d10} psychic damage each day acting against command (max once/day). Cannot command certain death. Dismiss anytime; {@spell remove curse}}, {@spell greater restoration}}, or {@spell wish}} also ends.' WHERE slug = 'geas';

UPDATE spells SET summary = 'Undo debilitating effect: reduce {@condition exhaustion}} by 1, or end charmed/petrified condition, curse (including cursed item attunement), ability score reduction, or HP maximum reduction.' WHERE slug = 'greater-restoration';

UPDATE spells SET summary = 'Touch point, infuse 60-foot-radius area with holy power. Celestials, elementals, fey, fiends, undead cannot enter; cannot charm/frighten/possess creatures within. Creatures already charmed/frightened/possessed: conditions end on entering. Choose extra effect: Courage (no {@condition frightened}}), Darkness, Daylight, Energy Protection (resistance), Energy Vulnerability, Everlasting Rest (undead become corpses), Sanctuary (Charisma save halves/negates effects).' WHERE slug = 'hallow';

UPDATE spells SET summary = 'Choose creature in range. {@dc} Wisdom save or become {@condition paralyzed}} for duration. No effect on undead. Target makes save again each turn ending, success ends spell.' WHERE slug = 'hold-monster';

UPDATE spells SET summary = 'Imbue weapon with holy power. Emits bright light 30 feet, dim 30 feet beyond. Weapon attacks deal +{@damage 2d8} radiant damage. Bonus action dismiss: burst of radiance, creatures in 30 feet {@dc} Constitution save or take {@damage 4d8} radiant damage and {@condition blinded}} 1 minute (half damage, not blinded on success; {@condition blinded}} creatures save end of turn).' WHERE slug = 'holy-weapon';

UPDATE spells SET summary = 'Swarming locusts fill 20-foot-radius sphere, {@quickref lightly obscured||3}}, {@quickref difficult terrain||3}}. Creatures entering or ending turn: {@dc} Constitution save or take {@damage 4d10} piercing damage (half on success).' WHERE slug = 'insect-plague';

UPDATE spells SET summary = 'Wave of healing from point you choose. Up to 6 creatures in 30-foot-radius sphere regain {@dice 3d8}} + spellcasting ability modifier HP. No effect on undead/constructs.' WHERE slug = 'mass-cure-wounds';

UPDATE spells SET summary = 'Ribbons of negative energy at creature. Non-undead: {@dc} Constitution save or take {@damage 5d12}} necrotic damage (half on success). Killed by damage: rises as {@creature zombie}} next turn. Undead target: no save, gains half {@dice 5d12}} as temporary HP.' WHERE slug = 'negative-energy-flood';

UPDATE spells SET summary = 'Passage appears in wood/plaster/stone surface: up to 5 feet wide, 8 feet tall, 20 feet deep. Lasts for duration. When passage disappears, creatures/objects ejected to nearest unoccupied space.' WHERE slug = 'passwall';

UPDATE spells SET summary = 'Forge telepathic link among up to 8 willing creatures. Intelligence 2 or less unaffected. Targets communicate telepathically regardless of language, any distance (not other planes).' WHERE slug = 'rary''s-telepathic-bond';

UPDATE spells SET summary = 'Transmute quiver producing endless nonmagical ammunition. Each turn, bonus action to make 2 ranged attacks using quiver. Ammunition magically replaces after each shot. Spell ends if quiver leaves your possession.' WHERE slug = 'swift-quiver';

UPDATE spells SET summary = 'Lightning bolt arcs to target, then 3 bolts leap to 3 other targets within 30 feet of first. Each target: {@dc} Dexterity save or take {@damage 10d8}} lightning damage (half on success). Cannot target same creature twice.' WHERE slug = 'chain-lightning';

UPDATE spells SET summary = 'Sphere of negative energy, 60-foot-radius from point. Creatures: {@dc} Constitution save or take {@damage 8d6}} necrotic damage (half on success).' WHERE slug = 'circle-of-death';

UPDATE spells SET summary = '10-foot-radius barrier around you. Blocks spells 5th level or lower from outside affecting creatures/objects within (even from higher slot). Spells can target barrier but have no effect inside.' WHERE slug = 'globe-of-invulnerability';

UPDATE spells SET summary = 'Unleash virulent disease on creature in range. {@dc} Constitution save or take {@damage 14d6}} necrotic damage (half on success). Damage cannot reduce HP below 1. Failed save: target''s HP maximum reduced 1 hour by damage amount. Disease removal restores HP maximum.' WHERE slug = 'harm';

UPDATE spells SET summary = 'Creature in range regains 70 HP. Ends {@condition blinded||blindness}}, {@condition deafened||deafness}}, diseases. No effect on constructs/undead.' WHERE slug = 'heal';

UPDATE spells SET summary = 'Negative energy through creature in range. {@dc} Constitution save or take {@damage 7d8 + 30}} necrotic damage (half on success). Humanoid killed: rises as {@creature zombie}} next turn, permanently under your command.' WHERE slug = 'finger-of-death';
