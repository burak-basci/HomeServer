import mods.modularmachinery.RecipeBuilder;

var fadingmatterrecipe = RecipeBuilder.newBuilder("fadingMatter", "matter_reactor", 6);

fadingmatterrecipe.addEnergyPerTickInput(500);
fadingmatterrecipe.addItemInput(<projectex:matter:10> * 3);
fadingmatterrecipe.addItemInput(<projectex:matter:9>);
fadingmatterrecipe.addItemOutput(<projectex:matter:11>);
fadingmatterrecipe.setChance(1);
fadingmatterrecipe.build();


var starshardrecipe = RecipeBuilder.newBuilder("finalstarshard", "starshard_replicator", 60);

starshardrecipe.addItemInput(<projectex:matter:11> * 4);
starshardrecipe.addItemInput(<projectex:matter:10> * 10);
starshardrecipe.addItemInput(<projectex:matter:9> * 6);
starshardrecipe.addItemInput(<projectex:power_flower:14>);
starshardrecipe.addItemOutput(<projectex:final_star_shard>);
starshardrecipe.setChance(1);
starshardrecipe.build();


var watchrecipe = RecipeBuilder.newBuilder("watch", "timetwisting_clocktower", 80);

watchrecipe.addEnergyPerTickInput(700);
watchrecipe.addFluidInput (<liquid:liquidlithium> * 1000); 
watchrecipe.addItemInput(<minecraft:clock>);
watchrecipe.addItemInput(<projecte:matter_block> * 8);
watchrecipe.addItemInput(<projectex:matter:4>* 5);
watchrecipe.addItemOutput(<projecte:item.pe_time_watch>);
watchrecipe.setChance(1);
watchrecipe.build();


var claymatterrecipe = RecipeBuilder.newBuilder("claymatter", "dissolving_chamber", 60);

claymatterrecipe.addEnergyPerTickInput(800);
claymatterrecipe.addItemInput(<mekanism:plasticblock:15> * 4);
claymatterrecipe.addItemInput(<projectex:compressed_collector:15>);
claymatterrecipe.addItemInput(<projectex:matter:11> * 3);
claymatterrecipe.addItemOutput(<projectex:clay_matter>);
claymatterrecipe.setChance(1);
claymatterrecipe.build();

var elytraduperecipe = RecipeBuilder.newBuilder("elytradupe", "dissolving_chamber", 40);

elytraduperecipe.addEnergyPerTickInput(500);
elytraduperecipe.addItemInput(<minecraft:elytra>);
elytraduperecipe.addItemInput(<minecraft:purpur_block> * 6);
elytraduperecipe.addItemInput(<projectex:matter:11> * 2);
elytraduperecipe.addItemInput(<projecte:fuel_block:2>);
elytraduperecipe.addItemOutput(<minecraft:elytra> * 2);
elytraduperecipe.setChance(1);
elytraduperecipe.build();


var finalstarrecipe = RecipeBuilder.newBuilder("star", "corrupted_starfactory", 120);

finalstarrecipe.addFluidInput (<liquid:liquidfusionfuel> * 1000); 
finalstarrecipe.addFluidInput (<liquid:liquidsulfurtrioxide> * 1000);
finalstarrecipe.addItemInput(<projectex:final_star_shard> * 8);
finalstarrecipe.addItemInput(<projectex:power_flower:15> * 2);
finalstarrecipe.addItemInput(<projectex:clay_matter>);
finalstarrecipe.addItemOutput(<projectex:final_star>);
finalstarrecipe.setChance(1);
finalstarrecipe.build();


var manapoolrecipe = RecipeBuilder.newBuilder("pool", "creative_assembler", 100);

manapoolrecipe.addFluidInput (<liquid:manyullyn> * 1000); 
manapoolrecipe.addFluidInput (<liquid:liquidhydrogenchloride> * 1000);
manapoolrecipe.addFluidInput (<liquid:liquidtritium> * 1000);
manapoolrecipe.addFluidInput (<liquid:sulfuricacid> * 1000);
manapoolrecipe.addFluidInput (<liquid:xu_evil_metal> * 1000);
manapoolrecipe.addFluidInput (<liquid:if.pink_slime> * 1000);
manapoolrecipe.addItemInput (<botania:pool:3>);
manapoolrecipe.addItemInput (<projectex:clay_matter> * 5);
manapoolrecipe.addItemInput (<projectex:final_star_shard> * 6);
manapoolrecipe.addItemInput (<teslacorelib:machine_case> * 8);
manapoolrecipe.addItemInput (<botania:flighttiara>);
manapoolrecipe.addItemInput (<xreliquary:witherless_rose>);
manapoolrecipe.addItemInput (<botania:storage:1> * 20);
manapoolrecipe.addItemInput (<xreliquary:emperor_chalice>);
manapoolrecipe.addItemInput (<projectex:colossal_star_omega>);
manapoolrecipe.addItemInput (<rootsclassic:flareorchid>);
manapoolrecipe.addItemOutput (<botania:pool:1>);
manapoolrecipe.setChance(1);
manapoolrecipe.build();

var archangelringrecipe = RecipeBuilder.newBuilder("archangel", "fusion_forge", 60);

archangelringrecipe.addEnergyPerTickInput(250);
archangelringrecipe.addFluidInput (<liquid:lava> * 1000); 
archangelringrecipe.addItemInput (<projecte:item.pe_ring_iron_band>);
archangelringrecipe.addItemInput (<projecte:matter_block> * 2);
archangelringrecipe.addItemInput (<minecraft:skull:1>);
archangelringrecipe.addItemInput (<minecraft:tipped_arrow>.withTag({Potion: "minecraft:harming"}));
archangelringrecipe.addItemOutput (<projecte:item.pe_archangel_smite>);
archangelringrecipe.setChance(1);
archangelringrecipe.build();

var zeroringrecipe = RecipeBuilder.newBuilder("zero", "fusion_forge", 60);

zeroringrecipe.addEnergyPerTickInput(250);
zeroringrecipe.addFluidInput (<liquid:water> * 1000); 
zeroringrecipe.addItemInput (<projecte:item.pe_ring_iron_band>);
zeroringrecipe.addItemInput (<projecte:matter_block> * 2);
zeroringrecipe.addItemInput (<minecraft:snow>);
zeroringrecipe.addItemInput (<xreliquary:mob_ingredient:10>);
zeroringrecipe.addItemOutput (<projecte:item.pe_zero_ring>);
zeroringrecipe.setChance(1);
zeroringrecipe.build();

var ignitionringrecipe = RecipeBuilder.newBuilder("ignition", "fusion_forge", 60);

ignitionringrecipe.addEnergyPerTickInput(250);
ignitionringrecipe.addFluidInput (<liquid:lava> * 1000); 
ignitionringrecipe.addItemInput (<projecte:item.pe_ring_iron_band>);
ignitionringrecipe.addItemInput (<projecte:matter_block> * 2);
ignitionringrecipe.addItemInput (<minecraft:flint_and_steel>);
ignitionringrecipe.addItemInput (<minecraft:fire_charge>);
ignitionringrecipe.addItemOutput (<projecte:item.pe_ignition>);
ignitionringrecipe.setChance(1);
ignitionringrecipe.build();

var blackholeringrecipe = RecipeBuilder.newBuilder("blackhole", "fusion_forge", 60);

blackholeringrecipe.addEnergyPerTickInput(250);
blackholeringrecipe.addFluidInput (<liquid:lava> * 1000); 
blackholeringrecipe.addItemInput (<projecte:item.pe_ring_iron_band>);
blackholeringrecipe.addItemInput (<projecte:matter_block> * 2);
blackholeringrecipe.addItemInput (<projecte:item.pe_matter>);
blackholeringrecipe.addItemInput (<minecraft:hopper>);
blackholeringrecipe.addItemOutput (<projecte:item.pe_black_hole>);
blackholeringrecipe.setChance(1);
blackholeringrecipe.build();

var flyringrecipe = RecipeBuilder.newBuilder("flyring", "fusion_forge", 60);

flyringrecipe.addEnergyPerTickInput(250);
flyringrecipe.addFluidInput (<liquid:lava> * 1000); 
flyringrecipe.addItemInput (<projecte:item.pe_ring_iron_band>);
flyringrecipe.addItemInput (<projecte:matter_block> * 2);
flyringrecipe.addItemInput (<minecraft:feather>);
flyringrecipe.addItemInput (<xreliquary:angelic_feather>);
flyringrecipe.addItemOutput (<projecte:item.pe_swrg>);
flyringrecipe.setChance(1);
flyringrecipe.build();

var harvestringrecipe = RecipeBuilder.newBuilder("harvest", "fusion_forge", 60);

harvestringrecipe.addEnergyPerTickInput(250);
harvestringrecipe.addFluidInput (<liquid:water> * 1000); 
harvestringrecipe.addItemInput (<projecte:item.pe_ring_iron_band>);
harvestringrecipe.addItemInput (<projecte:matter_block> * 2);
harvestringrecipe.addItemInput (<minecraft:hopper>);
harvestringrecipe.addItemInput (<minecraft:wheat_seeds> * 12);
harvestringrecipe.addItemOutput (<projecte:item.pe_harvest_god>);
harvestringrecipe.setChance(1);
harvestringrecipe.build();

var dmpedestalrecipe = RecipeBuilder.newBuilder("pedestal", "fusion_forge", 60);

dmpedestalrecipe.addEnergyPerTickInput(350);
dmpedestalrecipe.addFluidInput (<liquid:obsidian> * 1000); 
dmpedestalrecipe.addItemInput (<projecte:item.pe_matter:1> * 5);
dmpedestalrecipe.addItemInput (<projecte:item.pe_matter> * 10);
dmpedestalrecipe.addItemInput (<minecraft:armor_stand>);
dmpedestalrecipe.addItemOutput (<projecte:dm_pedestal>);
dmpedestalrecipe.setChance(1);
dmpedestalrecipe.build();

var emcchamberrecipe = RecipeBuilder.newBuilder("chamber", "fusion_forge", 100);

emcchamberrecipe.addEnergyPerTickInput(1000);
emcchamberrecipe.addFluidInput (<liquid:liquidtritium> * 1000); 
emcchamberrecipe.addItemInput (<projectex:compressed_refined_link> * 10);
emcchamberrecipe.addItemInput (<draconicevolution:awakened_core> * 5);
emcchamberrecipe.addItemInput (<projectex:arcane_tablet>);
emcchamberrecipe.addItemInput (<mekanism:atomicalloy> * 20);
emcchamberrecipe.addItemOutput (<equivalentintegrations:transmutation_chamber>);
emcchamberrecipe.setChance(1);
emcchamberrecipe.build();

var arcanetabletrecipe = RecipeBuilder.newBuilder("arcane", "matter_reactor", 60);

arcanetabletrecipe.addEnergyPerTickInput(200); 
arcanetabletrecipe.addItemInput (<minecraft:purple_shulker_box>);
arcanetabletrecipe.addItemInput (<projecte:item.pe_transmutation_tablet>);
arcanetabletrecipe.addItemInput (<projecte:item.pe_matter:1> * 7);
arcanetabletrecipe.addItemInput (<projectex:matter:1> * 2);
arcanetabletrecipe.addItemOutput (<projectex:arcane_tablet>);
arcanetabletrecipe.setChance(1);
arcanetabletrecipe.build();

var terminalrecipe = RecipeBuilder.newBuilder("terminal", "creative_assembler", 100);

terminalrecipe.addFluidInput (<liquid:liquidtritium> * 1000);
terminalrecipe.addFluidInput (<liquid:steam> * 1000);
terminalrecipe.addFluidInput (<liquid:sewage> * 1000); 
terminalrecipe.addFluidInput (<liquid:biofuel> * 1000); 
terminalrecipe.addFluidInput (<liquid:essence> * 1000); 
terminalrecipe.addFluidInput (<liquid:xu_demonic_metal> * 1000); 
terminalrecipe.addItemInput (<wct:wct>);
terminalrecipe.addItemInput (<xreliquary:salamander_eye>);
terminalrecipe.addItemInput (<projectex:clay_matter> * 12);
terminalrecipe.addItemInput (<projectex:final_star_shard> * 7);
terminalrecipe.addItemInput (<appliedenergistics2:material:47> *  8);
terminalrecipe.addItemInput (<teslacorelib:machine_case> * 5);
terminalrecipe.addItemInput (<mekanism:basicblock:8> * 50);
terminalrecipe.addItemInput (<mekanism:teleportationcore> * 40);
terminalrecipe.addItemInput (<projectex:arcane_tablet>);
terminalrecipe.addItemInput (<extrautils2:opinium:8> *4);
terminalrecipe.addItemOutput (<wct:wct_creative>);
terminalrecipe.setChance(1);
terminalrecipe.build();

var alchemytablerecipe = RecipeBuilder.newBuilder("alchemytable", "matter_reactor", 60);

alchemytablerecipe.addEnergyPerTickInput(250);
alchemytablerecipe.addItemInput(<projectex:energy_link>);
alchemytablerecipe.addItemInput(<minecraft:crafting_table>);
alchemytablerecipe.addItemInput(<projecte:transmutation_table>);
alchemytablerecipe.addItemOutput(<projectex:alchemy_table>);
alchemytablerecipe.setChance(1);
alchemytablerecipe.build();

var drumrecipe = RecipeBuilder.newBuilder("drum", "creative_assembler", 100);

drumrecipe.addFluidInput (<liquid:liquidsulfurtrioxide> * 1000);
drumrecipe.addFluidInput (<liquid:liquidfusionfuel> * 1000);
drumrecipe.addFluidInput (<liquid:heavywater> * 1000);
drumrecipe.addFluidInput (<liquid:pigiron> * 1000);
drumrecipe.addFluidInput (<liquid:biofuel> * 1000);
drumrecipe.addFluidInput (<liquid:liquidhydrogenchloride> *1000);
drumrecipe.addItemInput (<mekanism:controlcircuit:3> * 60);
drumrecipe.addItemInput (<projectex:final_star> * 2);
drumrecipe.addItemInput (<projectex:clay_matter> * 22);
drumrecipe.addItemInput (<extrautils2:drum:3> * 45);
drumrecipe.addItemInput (<mekanism:plasticblock:15> * 25);
drumrecipe.addItemInput (<projectex:power_flower:15> *7);
drumrecipe.addItemInput (<projectex:colossal_star_omega>);
drumrecipe.addItemInput (<hammercore:gold_bordered_cobblestone>);
drumrecipe.addItemInput (<teslacorelib:machine_case> * 5);
drumrecipe.addItemOutput (<mekanism:machineblock2:11>.withTag({tier: 4}));
drumrecipe.setChance(1);
drumrecipe.build();

var storagerecipe = RecipeBuilder.newBuilder("storage", "creative_assembler", 100);

storagerecipe.addFluidInput (<liquid:liquidoxygen> * 1000); 
storagerecipe.addFluidInput (<liquid:liquidhydrogenchloride> * 1000); 
storagerecipe.addFluidInput (<liquid:liquidtritium> * 1000); 
storagerecipe.addFluidInput (<liquid:liquiddeuterium> * 1000); 
storagerecipe.addFluidInput (<liquid:cobalt> * 1000);
storagerecipe.addFluidInput (<liquid:liquidfusionfuel> * 1000);
storagerecipe.addItemInput (<appliedenergistics2:storage_cell_64k>);
storagerecipe.addItemInput (<teslacorelib:machine_case> * 10);
storagerecipe.addItemInput (<xreliquary:phoenix_down>);
storagerecipe.addItemInput (<appliedenergistics2:material:47> * 45);
storagerecipe.addItemInput (<projectex:power_flower:15> * 10);
storagerecipe.addItemInput (<projectex:final_star>);
storagerecipe.addItemInput (<projectex:colossal_star_omega>);
storagerecipe.addItemInput (<botania:manaresource:5> * 32);
storagerecipe.addItemInput (<projectex:clay_matter> * 20);
storagerecipe.addItemInput (<hammercore:quartz_bordered_cobblestone>);
storagerecipe.addItemOutput (<appliedenergistics2:creative_storage_cell>);
storagerecipe.setChance(1);
storagerecipe.build();

var millrecipe = RecipeBuilder.newBuilder("mill", "creative_assembler", 100);

millrecipe.addFluidInput (<liquid:xu_evil_metal> * 1000); 
millrecipe.addFluidInput (<liquid:xu_demonic_metal> * 1000);
millrecipe.addFluidInput (<liquid:xu_enchanted_metal> * 1000);
millrecipe.addFluidInput (<liquid:liquidsulfurtrioxide> * 1000);
millrecipe.addFluidInput (<liquid:biofuel> * 1000);
millrecipe.addFluidInput (<liquid:liquidhydrogenchloride> * 1000);
millrecipe.addItemInput (<teslacorelib:machine_case> * 3);
millrecipe.addItemInput (<xreliquary:mob_ingredient:5> * 5);
millrecipe.addItemInput (<projectex:matter:11> * 40);
millrecipe.addItemInput (<projectex:colossal_star_omega> * 2);
millrecipe.addItemInput (<projectex:final_star_shard> * 3);
millrecipe.addItemInput (<extrautils2:opinium:8> * 6);
millrecipe.addItemInput (<extrautils2:passivegenerator:8> * 7);
millrecipe.addItemInput (<extrautils2:ingredients:16> * 2);
millrecipe.addItemInput (<totemic:baykok_bow>);
millrecipe.addItemOutput (<extrautils2:passivegenerator:6>);
millrecipe.setChance(1);
millrecipe.build();

var spikerecipe = RecipeBuilder.newBuilder("spike", "creative_assembler", 100);

spikerecipe.addFluidInput (<liquid:emerald> * 1000); 
spikerecipe.addFluidInput (<liquid:steel> * 1000);
spikerecipe.addFluidInput (<liquid:manyullyn> * 1000); 
spikerecipe.addFluidInput (<liquid:gold> * 1000); 
spikerecipe.addFluidInput (<liquid:ardite> * 1000); 
spikerecipe.addFluidInput (<liquid:glass> * 1000); 
spikerecipe.addItemInput (<rootsclassic:livingsword>);
spikerecipe.addItemInput (<xreliquary:magicbane>);
spikerecipe.addItemInput (<projecte:item.pe_dm_sword>);
spikerecipe.addItemInput (<projecte:item.pe_rm_sword>);
spikerecipe.addItemInput (<appliedenergistics2:certus_quartz_sword>);
spikerecipe.addItemInput (<botania:manasteelsword>);
spikerecipe.addItemInput (<minecraft:diamond_sword>);
spikerecipe.addItemInput (<minecraft:golden_sword>);
spikerecipe.addItemInput (<botania:elementiumsword>);
spikerecipe.addItemInput (<xreliquary:midas_touchstone>);
spikerecipe.addItemOutput (<extrautils2:spike_creative>);
spikerecipe.setChance(1);
spikerecipe.build();

var energyrecipe = RecipeBuilder.newBuilder("energy", "creative_assembler", 100);

energyrecipe.addFluidInput (<liquid:heavywater> * 1000); 
energyrecipe.addFluidInput (<liquid:blood> * 1000);
energyrecipe.addFluidInput (<liquid:essence> * 1000);
energyrecipe.addFluidInput (<liquid:liquidlithium> * 1000);
energyrecipe.addFluidInput (<liquid:liquidsulfurdioxide> * 1000);
energyrecipe.addFluidInput (<liquid:sulfuricacid> * 1000);
energyrecipe.addItemInput (<appliedenergistics2:dense_energy_cell>);
energyrecipe.addItemInput (<appliedenergistics2:spatial_storage_cell_128_cubed>);
energyrecipe.addItemInput (<fluxnetworks:fluxblock> * 60);
energyrecipe.addItemInput (<rootsclassic:midnightbloom>);
energyrecipe.addItemInput (<teslacorelib:machine_case> * 3);
energyrecipe.addItemInput (<projectex:clay_matter> * 12);
energyrecipe.addItemInput (<projectex:final_star_shard> * 4);
energyrecipe.addItemInput (<botania:rune:13> * 40);
energyrecipe.addItemInput (<botania:divacharm>);
energyrecipe.addItemInput (<botania:flighttiara>);
energyrecipe.addItemOutput (<appliedenergistics2:creative_energy_cell>);
energyrecipe.setChance(1);
energyrecipe.build();

var wandrecipe = RecipeBuilder.newBuilder("wand", "creative_assembler", 100);

wandrecipe.addFluidInput (<liquid:xpjuice> * 1000); 
wandrecipe.addFluidInput (<liquid:cobalt> * 1000);
wandrecipe.addFluidInput (<liquid:liquidsodium>* 1000);
wandrecipe.addFluidInput (<liquid:liquidethene>* 1000);
wandrecipe.addFluidInput (<liquid:blood> * 1000);
wandrecipe.addFluidInput (<liquid:lava> * 1000);
wandrecipe.addItemInput (<extrautils2:itembuilderswand>);
wandrecipe.addItemInput (<projectex:compressed_collector:14> * 6);
wandrecipe.addItemInput (<projectex:clay_matter> * 4);
wandrecipe.addItemInput (<extrautils2:decorativesolid:8> *32);
wandrecipe.addItemInput (<botania:rainbowrod>);
wandrecipe.addItemInput (<xreliquary:glacial_staff>);
wandrecipe.addItemInput (<xreliquary:mob_ingredient:8> * 5);
wandrecipe.addItemInput (<mekanism:ingot> * 32);
wandrecipe.addItemInput (<teslacorelib:machine_case> * 3);
wandrecipe.addItemInput (<xreliquary:mercy_cross>);
wandrecipe.addItemOutput (<extrautils2:itemcreativebuilderswand>);
wandrecipe.setChance(1);
wandrecipe.build();

var infdrawerrecipe = RecipeBuilder.newBuilder("drawer", "creative_assembler", 100);

infdrawerrecipe.addFluidInput (<liquid:liquidfusionfuel> * 1000); 
infdrawerrecipe.addFluidInput (<liquid:xu_demonic_metal> * 1000);
infdrawerrecipe.addFluidInput (<liquid:ardite> * 1000); 
infdrawerrecipe.addFluidInput (<liquid:manyullyn> * 1000); 
infdrawerrecipe.addFluidInput (<liquid:pigiron> * 1000);
infdrawerrecipe.addFluidInput (<liquid:liquidhydrogenchloride> *1000);
infdrawerrecipe.addItemInput (<storagedrawers:upgrade_storage:4>);
infdrawerrecipe.addItemInput (<hammercore:emerald_bordered_cobblestone>);
infdrawerrecipe.addItemInput (<totemic:ceremony_cheat>);
infdrawerrecipe.addItemInput (<botania:manaresource:14> * 20);
infdrawerrecipe.addItemInput (<projecte:item.pe_time_watch>);
infdrawerrecipe.addItemInput (<teslacorelib:machine_case> * 40);
infdrawerrecipe.addItemInput (<projectex:compressed_collector:15> * 20);
infdrawerrecipe.addItemInput (<projectex:final_star>);
infdrawerrecipe.addItemInput (<projectex:power_flower:15> * 15);
infdrawerrecipe.addItemInput (<mekanism:controlcircuit:3> * 50);
infdrawerrecipe.addItemOutput (<storagedrawers:upgrade_creative:1> * 2);
infdrawerrecipe.setChance(1);
infdrawerrecipe.build();

var omegastarrecipe = RecipeBuilder.newBuilder("colossalstar", "corrupted_starfactory", 60);
omegastarrecipe.addFluidInput (<liquid:xu_evil_metal> * 1000);
omegastarrecipe.addItemInput (<projectex:colossal_star_sphere> * 4);
omegastarrecipe.addItemOutput (<projectex:colossal_star_omega>);
omegastarrecipe.setChance(1);
omegastarrecipe.build();

//Botanical Infuser

var harvestrodrecipe = RecipeBuilder.newBuilder("harvestrod", "botanical_infuser", 100);
harvestrodrecipe.addEnergyPerTickInput(400);
harvestrodrecipe.addFluidInput (<liquid:essence> * 1000);
harvestrodrecipe.addItemInput (<minecraft:blaze_rod>);
harvestrodrecipe.addItemInput (<minecraft:vine> * 4);
harvestrodrecipe.addItemInput (<xreliquary:void_tear>);
harvestrodrecipe.addItemInput (<rootsclassic:mutagen>);
harvestrodrecipe.addItemOutput (<xreliquary:harvest_rod>);
harvestrodrecipe.setChance(1);
harvestrodrecipe.build();

var xpbottlerecipe = RecipeBuilder.newBuilder("xpbottle", "botanical_infuser", 20);
xpbottlerecipe.addEnergyPerTickInput(100);
xpbottlerecipe.addFluidInput (<liquid:essence> * 1000);
xpbottlerecipe.addItemInput (<minecraft:glass_bottle>);
xpbottlerecipe.addItemOutput (<minecraft:experience_bottle>);
xpbottlerecipe.setChance(1);
xpbottlerecipe.build();

var cheatceremonyrecipe = RecipeBuilder.newBuilder("cheatceremony", "botanical_infuser", 100);
cheatceremonyrecipe.addEnergyPerTickInput(1200);
cheatceremonyrecipe.addFluidInput (<liquid:if.pink_slime> * 1000);
cheatceremonyrecipe.addItemInput (<totemic:totemic_staff>);
cheatceremonyrecipe.addItemInput (<totemic:eagle_drops:1> * 2);
cheatceremonyrecipe.addItemInput (<totemic:cooked_buffalo_meat> * 2);
cheatceremonyrecipe.addItemInput (<totemic:eagle_drops> * 2);
cheatceremonyrecipe.addItemOutput (<totemic:ceremony_cheat>);
cheatceremonyrecipe.setChance(1);
cheatceremonyrecipe.build();

var dandelifeonrecipe = RecipeBuilder.newBuilder("botaniaflower", "botanical_infuser", 60);
dandelifeonrecipe.addEnergyPerTickInput(400);
dandelifeonrecipe.addFluidInput (<liquid:xu_demonic_metal> * 1000);
dandelifeonrecipe.addItemInput (<botania:rune:13>);
dandelifeonrecipe.addItemInput (<botania:rune:15>);
dandelifeonrecipe.addItemInput (<botania:rune:14>);
dandelifeonrecipe.addItemInput (<botania:manaresource:5>);
dandelifeonrecipe.addItemOutput (<botania:specialflower>.withTag({type: "dandelifeon"}));
dandelifeonrecipe.setChance(1);
dandelifeonrecipe.build();

var charmrecipe = RecipeBuilder.newBuilder("charmbotania", "botanical_infuser", 60);
charmrecipe.addEnergyPerTickInput(400);
charmrecipe.addFluidInput (<liquid:gold> * 1000);
charmrecipe.addItemInput (<botania:manaresource:5> * 2);
charmrecipe.addItemInput (<minecraft:gold_block> * 3);
charmrecipe.addItemInput (<botania:tinyplanet>);
charmrecipe.addItemInput (<botania:rune:15>);
charmrecipe.addItemOutput (<botania:divacharm>);
charmrecipe.setChance(1);
charmrecipe.build();

var spiritduperecipe = RecipeBuilder.newBuilder("spiritdupe", "botanical_infuser", 40);
spiritduperecipe.addEnergyPerTickInput(500);
spiritduperecipe.addFluidInput (<liquid:manyullyn> * 1000);
spiritduperecipe.addItemInput (<botania:manaresource:7> * 5);
spiritduperecipe.addItemInput (<botania:manaresource:4> * 10);
spiritduperecipe.addItemInput (<botania:manaresource:8> * 5);
spiritduperecipe.addItemInput (<botania:manaresource:5>);
spiritduperecipe.addItemOutput (<botania:manaresource:5> * 2);
spiritduperecipe.setChance(1);
spiritduperecipe.build();

//Sacrificial Crystal

var witherskeletonheadrecipe = RecipeBuilder.newBuilder("witherskull", "sacrificial_crystal", 40);
witherskeletonheadrecipe.addEnergyPerTickInput(200);
witherskeletonheadrecipe.addFluidInput (<liquid:blood> * 1000);
witherskeletonheadrecipe.addItemInput (<darkutils:material>);
witherskeletonheadrecipe.addItemInput (<minecraft:bone> * 8);
witherskeletonheadrecipe.addItemOutput (<minecraft:skull:1>);
witherskeletonheadrecipe.setChance(1);
witherskeletonheadrecipe.build();

var witherroserecipe = RecipeBuilder.newBuilder("witherrose", "sacrificial_crystal", 100);
witherroserecipe.addEnergyPerTickInput(400);
witherroserecipe.addFluidInput (<liquid:blood> * 1000);
witherroserecipe.addItemInput (<minecraft:nether_star> * 4);
witherroserecipe.addItemInput (<minecraft:double_plant:4>);
witherroserecipe.addItemInput (<xreliquary:mob_ingredient:9> * 4);
witherroserecipe.addItemOutput (<xreliquary:witherless_rose>);
witherroserecipe.setChance(1);
witherroserecipe.build();

var batwingrecipe = RecipeBuilder.newBuilder("batwing", "sacrificial_crystal", 60);
batwingrecipe.addEnergyPerTickInput(400);
batwingrecipe.addFluidInput (<liquid:blood> * 1000);
batwingrecipe.addItemInput (<minecraft:feather>);
batwingrecipe.addItemInput (<botania:dye:15>);
batwingrecipe.addItemInput (<minecraft:potion>.withTag({Potion: "extrautils2:xu2.gravity"}));
batwingrecipe.addItemInput (<projectex:matter:3>);
batwingrecipe.addItemOutput (<xreliquary:mob_ingredient:5>);
batwingrecipe.setChance(1);
batwingrecipe.build();

var slimepearlrecipe = RecipeBuilder.newBuilder("slimepearl", "sacrificial_crystal", 60);
slimepearlrecipe.addEnergyPerTickInput(200);
slimepearlrecipe.addFluidInput (<liquid:blood> * 1000);
slimepearlrecipe.addItemInput (<minecraft:slime_ball> * 8);
slimepearlrecipe.addItemInput (<extrautils2:ingredients:12>);
slimepearlrecipe.addItemOutput (<xreliquary:mob_ingredient:4>);
slimepearlrecipe.setChance(1);
slimepearlrecipe.build();

var squidbeakrecipe = RecipeBuilder.newBuilder("squidbeak", "sacrificial_crystal", 60);
squidbeakrecipe.addEnergyPerTickInput(200);
squidbeakrecipe.addFluidInput (<liquid:blood> * 1000);
squidbeakrecipe.addItemInput (<minecraft:dye>);
squidbeakrecipe.addItemInput (<botania:manabottle>);
squidbeakrecipe.addItemOutput (<xreliquary:mob_ingredient:12>);
squidbeakrecipe.setChance(1);
squidbeakrecipe.build();

var nethereyerecipe = RecipeBuilder.newBuilder("salamandereye", "sacrificial_crystal", 100);
nethereyerecipe.addEnergyPerTickInput(500);
nethereyerecipe.addFluidInput (<liquid:blood> * 1000);
nethereyerecipe.addItemInput (<botania:thirdeye>);
nethereyerecipe.addItemInput (<xreliquary:mob_ingredient:10>);
nethereyerecipe.addItemInput (<xreliquary:mob_ingredient:11>);
nethereyerecipe.addItemInput (<xreliquary:mob_ingredient:7>);
nethereyerecipe.addItemOutput (<xreliquary:salamander_eye>);
nethereyerecipe.setChance(1);
nethereyerecipe.build();

var netherfeatherrecipe = RecipeBuilder.newBuilder("phoenixdown", "sacrificial_crystal", 100);
netherfeatherrecipe.addEnergyPerTickInput(500);
netherfeatherrecipe.addFluidInput (<liquid:blood> * 1000);
netherfeatherrecipe.addItemInput (<xreliquary:angelic_feather>);
netherfeatherrecipe.addItemInput (<minecraft:potion>.withTag({Potion: "minecraft:strong_regeneration"}));
netherfeatherrecipe.addItemInput (<xreliquary:kraken_shell>);
netherfeatherrecipe.addItemInput (<projecte:item.pe_life_stone>);
netherfeatherrecipe.addItemOutput (<xreliquary:phoenix_down>);
netherfeatherrecipe.setChance(1);
netherfeatherrecipe.build();

var draconicmanipulatorrecipe = RecipeBuilder.newBuilder("weathermanipulator", "timetwisting_clocktower", 120);
draconicmanipulatorrecipe.addEnergyPerTickInput(300);
draconicmanipulatorrecipe.addFluidInput (<liquid:manyullyn> * 1000);
draconicmanipulatorrecipe.addItemInput (<draconicevolution:wyvern_core> * 2);
draconicmanipulatorrecipe.addItemInput (<minecraft:dragon_egg>);
draconicmanipulatorrecipe.addItemInput (<draconicevolution:draconium_ingot> * 6);
draconicmanipulatorrecipe.addItemOutput (<draconicevolution:celestial_manipulator>);
draconicmanipulatorrecipe.setChance(1);
draconicmanipulatorrecipe.build();

var refinedenergyrecipe = RecipeBuilder.newBuilder("refinedenergy", "refined_generator", 1);
refinedenergyrecipe.addFluidInput (<liquid:liquidsulfurtrioxide> * 1000);
refinedenergyrecipe.addEnergyPerTickOutput(7500000);
refinedenergyrecipe.build();

var solidxptoliquid = RecipeBuilder.newBuilder("liquidxp", "dissolving_chamber", 5);

solidxptoliquid.addEnergyPerTickInput(300);
solidxptoliquid.addItemInput(<morechickens:solidxp>);
solidxptoliquid.addFluidOutput(<liquid:xpjuice> * 100);
solidxptoliquid.setChance(1);
solidxptoliquid.build();

//Monolith of reversing recipes

var relayfuse = RecipeBuilder.newBuilder("relayfuse", "monolith_of_reversing", 30);
relayfuse.addFluidInput (<liquid:liquidsodium> * 1000);
relayfuse.addItemInput (<draconicevolution:draconium_block:1>);
relayfuse.addItemOutput (<teslacorelib:machine_case>);
relayfuse.setChance(1);
relayfuse.build();

var chickentoeagle = RecipeBuilder.newBuilder("eagleegg", "monolith_of_reversing", 50);
chickentoeagle.addFluidInput (<liquid:meat> * 1000);
chickentoeagle.addItemInput (<minecraft:spawn_egg>.withTag({EntityTag: {id: "minecraft:chicken"}}));
chickentoeagle.addItemOutput (<minecraft:spawn_egg>.withTag({EntityTag: {id: "totemic:bald_eagle"}}));
chickentoeagle.setChance(1);
chickentoeagle.build();

var cowtobuffalo = RecipeBuilder.newBuilder("buffaloegg", "monolith_of_reversing", 50);
cowtobuffalo.addFluidInput (<liquid:meat> * 1000);
cowtobuffalo.addItemInput (<minecraft:spawn_egg>.withTag({EntityTag: {id: "minecraft:cow"}}));
cowtobuffalo.addItemOutput (<minecraft:spawn_egg>.withTag({EntityTag: {id: "totemic:buffalo"}}));
cowtobuffalo.setChance(1);
cowtobuffalo.build();

var slimesapling = RecipeBuilder.newBuilder("slimesapling", "monolith_of_reversing", 20);
slimesapling.addFluidInput (<liquid:molten_reinforced_pink_slime> * 1000);
slimesapling.addItemInput (<minecraft:sapling>);
slimesapling.addItemOutput (<tconstruct:slime_sapling:1>);
slimesapling.setChance(1);
slimesapling.build();

//FlowerEnhancer recipes

var recipemidnightbloom = RecipeBuilder.newBuilder("midnightbloom", "flower_enhancer", 60);
recipemidnightbloom.addEnergyPerTickInput(400);
recipemidnightbloom.addItemInput (<rootsclassic:mutagen> * 10);
recipemidnightbloom.addItemInput (<minecraft:red_flower:1>);
recipemidnightbloom.addItemInput (<extrautils2:ingredients:5>);
recipemidnightbloom.addItemInput (<botania:rune:13>);
recipemidnightbloom.addItemOutput (<rootsclassic:midnightbloom>);
recipemidnightbloom.setChance(1);
recipemidnightbloom.build();

var reciperadiantdaisy = RecipeBuilder.newBuilder("radiantdaisy", "flower_enhancer", 60);
reciperadiantdaisy.addEnergyPerTickInput(400);
reciperadiantdaisy.addItemInput (<rootsclassic:mutagen> * 10);
reciperadiantdaisy.addItemInput (<minecraft:red_flower:8>);
reciperadiantdaisy.addItemInput (<botania:quartz:6>);
reciperadiantdaisy.addItemInput (<botania:rune:3>);
reciperadiantdaisy.addItemOutput (<rootsclassic:radiantdaisy>);
reciperadiantdaisy.setChance(1);
reciperadiantdaisy.build();

var recipeflareochid = RecipeBuilder.newBuilder("flareorchid", "flower_enhancer", 60);
recipeflareochid.addEnergyPerTickInput(400);
recipeflareochid.addItemInput (<rootsclassic:mutagen> * 10);
recipeflareochid.addItemInput (<minecraft:red_flower:4>);
recipeflareochid.addItemInput (<minecraft:nether_star>);
recipeflareochid.addItemInput (<botania:rune:1>);
recipeflareochid.addItemOutput (<rootsclassic:flareorchid>);
recipeflareochid.setChance(1);
recipeflareochid.build();

//Botania Tweaks

mods.botania.RuneAltar.addRecipe(<modularmachinery:blockcontroller>, [<mekanism:basicblock:8>, <projectex:matter:2>, <botania:manaresource:4>, <industrialforegoing:plastic>, <enderio:item_material:20>, <draconicevolution:draconic_core>, <appliedenergistics2:material:24>, <tconstruct:ingots:2>], 20000);
mods.botania.Apothecary.removeRecipe(<botania:specialflower>.withTag({type: "dandelifeon"}));

//Mekanism Tweaks

mods.mekanism.crusher.addRecipe(<minecraft:ender_pearl>, <appliedenergistics2:material:46>);

//EnderIO Tweaks

mods.enderio.AlloySmelter.addRecipe(<appliedenergistics2:material:1>, [<appliedenergistics2:material:2>, <enderio:item_alloy_ingot>, <fluxnetworks:flux>]);

//JEI Tweaks
mods.jei.JEI.addDescription(<draconicevolution:dragon_heart>,"Can be obtained by slaying the Ender Dragon.");
mods.jei.JEI.addDescription(<roost:chicken>.withTag({Growth: 1, Chicken: "morechickens:funwaychick", Gain: 1, Strength: 1}),"Creating this chicken requires feeding TNT to a vanilla chicken.");
mods.jei.JEI.addDescription(<liquid:heavywater>,"Obtained by installing a filter upgrade into an electric pump.");
mods.jei.JEI.addDescription(<botania:manaresource:5>,"Obtained by killing the Gaia boss, can be duped in the Botanical Infuser.");
mods.jei.JEI.addDescription(<draconicevolution:chaos_shard>,"Chaos islands don't spawn in the End. The only way to obtain this item is by making it using fusion crafting.");
mods.jei.JEI.addDescription(<liquid:essence>,"Essence is made inside the Mob Crusher when it kills a mob.");
mods.jei.JEI.addDescription(<liquid:sewage>,"You can obtain sewage from the Animal Sewer if an animal stands on top of it.");
mods.jei.JEI.addDescription(<liquid:sludge>,"Made in Sludge Refiner.");
mods.jei.JEI.addDescription(<liquid:steam>,"Made inside a special multiblock structure called Thermoelectric Boiler that is exclusive to Mekanism.");
mods.jei.JEI.addDescription(<rootsclassic:radiantdaisy>,"The original ritual was disabled. Use the machine recipe.");
mods.jei.JEI.addDescription(<rootsclassic:midnightbloom>,"The original ritual was disabled. Use the machine recipe.");
mods.jei.JEI.addDescription(<rootsclassic:flareorchid>,"The original ritual was disabled. Use the machine recipe.");
mods.jei.JEI.addDescription(<xreliquary:mob_ingredient:8>,"This item can be easily obtained by using a Storm Shot.");
mods.jei.JEI.addDescription(<minecraft:spawn_egg>.withTag({EntityTag: {id: "totemic:bald_eagle"}}),"This recipe is irrelevant unless you already finished all Endgame Challenges. Use a totemic ritual to obtain this mob.");
mods.jei.JEI.addDescription(<minecraft:spawn_egg>.withTag({EntityTag: {id: "totemic:buffalo"}}),"This recipe is irrelevant unless you already finished all Endgame Challenges. Use a totemic ritual to obtain this mob.");

//Vanilla Tools Changes

<minecraft:golden_axe>.maxDamage = 1;
<minecraft:golden_shovel>.maxDamage = 1;
<minecraft:golden_hoe>.maxDamage = 1;
<minecraft:golden_pickaxe>.maxDamage = 1;
<minecraft:golden_sword>.maxDamage = 1;
	
<minecraft:diamond_shovel>.maxDamage = 1;
<minecraft:diamond_axe>.maxDamage = 1;
<minecraft:diamond_pickaxe>.maxDamage = 1;
<minecraft:diamond_hoe>.maxDamage = 1;
<minecraft:diamond_sword>.maxDamage = 1;
	
<minecraft:iron_shovel>.maxDamage = 1;
<minecraft:iron_axe>.maxDamage = 1;
<minecraft:iron_pickaxe>.maxDamage = 1;
<minecraft:iron_hoe>.maxDamage = 1;
<minecraft:iron_sword>.maxDamage = 1;
		
<minecraft:wooden_pickaxe>.maxDamage = 1;
<minecraft:wooden_sword>.maxDamage = 1;
<minecraft:wooden_hoe>.maxDamage = 1;
<minecraft:wooden_shovel>.maxDamage = 1;
<minecraft:wooden_axe>.maxDamage = 1;
	
<minecraft:stone_pickaxe>.maxDamage = 1;
<minecraft:stone_hoe>.maxDamage = 1;
<minecraft:stone_axe>.maxDamage = 1;
<minecraft:stone_shovel>.maxDamage = 1;
<minecraft:stone_sword>.maxDamage = 1;

<minecraft:golden_axe>.addTooltip(format.red("Vanilla tools are fragile. Use Tinkers' Construct tools."));
<minecraft:golden_shovel>.addTooltip(format.red("Vanilla tools are fragile. Use Tinkers' Construct tools."));
<minecraft:golden_hoe>.addTooltip(format.red("Vanilla tools are fragile. Use Tinkers' Construct tools."));
<minecraft:golden_pickaxe>.addTooltip(format.red("Vanilla tools are fragile. Use Tinkers' Construct tools."));
<minecraft:golden_sword>.addTooltip(format.red("Vanilla tools are fragile. Use Tinkers' Construct tools."));
	
<minecraft:diamond_shovel>.addTooltip(format.red("Vanilla tools are fragile. Use Tinkers' Construct tools."));
<minecraft:diamond_axe>.addTooltip(format.red("Vanilla tools are fragile. Use Tinkers' Construct tools."));
<minecraft:diamond_pickaxe>.addTooltip(format.red("Vanilla tools are fragile. Use Tinkers' Construct tools."));
<minecraft:diamond_hoe>.addTooltip(format.red("Vanilla tools are fragile. Use Tinkers' Construct tools."));
<minecraft:diamond_sword>.addTooltip(format.red("Vanilla tools are fragile. Use Tinkers' Construct tools."));
	
<minecraft:iron_shovel>.addTooltip(format.red("Vanilla tools are fragile. Use Tinkers' Construct tools."));
<minecraft:iron_axe>.addTooltip(format.red("Vanilla tools are fragile. Use Tinkers' Construct tools."));
<minecraft:iron_pickaxe>.addTooltip(format.red("Vanilla tools are fragile. Use Tinkers' Construct tools."));
<minecraft:iron_hoe>.addTooltip(format.red("Vanilla tools are fragile. Use Tinkers' Construct tools."));
<minecraft:iron_sword>.addTooltip(format.red("Vanilla tools are fragile. Use Tinkers' Construct tools."));
		
<minecraft:wooden_pickaxe>.addTooltip(format.red("Vanilla tools are fragile. Use Tinkers' Construct tools."));
<minecraft:wooden_sword>.addTooltip(format.red("Vanilla tools are fragile. Use Tinkers' Construct tools."));
<minecraft:wooden_hoe>.addTooltip(format.red("Vanilla tools are fragile. Use Tinkers' Construct tools."));
<minecraft:wooden_shovel>.addTooltip(format.red("Vanilla tools are fragile. Use Tinkers' Construct tools."));
<minecraft:wooden_axe>.addTooltip(format.red("Vanilla tools are fragile. Use Tinkers' Construct tools."));
	
<minecraft:stone_pickaxe>.addTooltip(format.red("Vanilla tools are fragile. Use Tinkers' Construct tools."));
<minecraft:stone_hoe>.addTooltip(format.red("Vanilla tools are fragile. Use Tinkers' Construct tools."));
<minecraft:stone_axe>.addTooltip(format.red("Vanilla tools are fragile. Use Tinkers' Construct tools."));
<minecraft:stone_shovel>.addTooltip(format.red("Vanilla tools are fragile. Use Tinkers' Construct tools."));
<minecraft:stone_sword>.addTooltip(format.red("Vanilla tools are fragile. Use Tinkers' Construct tools."));



//Remove
recipes.remove(<projecte:item.pe_philosophers_stone>);
recipes.remove(<aroma1997sdimension:dimensionchanger>);
recipes.remove(<projectex:stone_table>);
recipes.remove(<aroma1997sdimension:portalframe>);
recipes.remove(<aroma1997sdimension:miningmultitool>);
recipes.remove(<projecte:transmutation_table>);
recipes.remove(<minecraft:end_portal_frame>);
recipes.remove(<tconstruct:soil>);
recipes.remove(<rootsclassic:livingsword>);
recipes.remove(<modularmachinery:itemmodularium>);
recipes.remove(<projectex:matter:11>);
recipes.remove(<modularmachinery:blockcasing:4>);
recipes.remove(<projectex:final_star_shard>);
recipes.remove(<projectex:relay:15>);
recipes.remove(<projecte:item.pe_time_watch>);
recipes.remove(<projectex:final_star>);
recipes.remove(<projectex:clay_matter>);
recipes.remove(<projecte:item.pe_archangel_smite>);
recipes.remove(<projecte:item.pe_zero_ring>);
recipes.remove(<projecte:item.pe_ignition>);
recipes.remove(<projecte:item.pe_black_hole>);
recipes.remove(<projecte:item.pe_swrg>);
recipes.remove(<projecte:item.pe_harvest_god>);
recipes.remove(<projecte:item.pe_life_stone>);
recipes.remove(<projecte:dm_pedestal>);
recipes.remove(<projectex:arcane_tablet>);
recipes.remove(<projectex:alchemy_table>);
recipes.remove(<modularmachinery:blockcontroller>);
recipes.remove(<botania:invisibilitycloak>);
recipes.remove(<mekanism:basicblock:8>);
recipes.remove(<teslacorelib:machine_case>);
recipes.remove(<harvestcraft:freshwateritem>);
recipes.remove(<xreliquary:mob_ingredient:12>);
recipes.remove(<xreliquary:phoenix_down>);
recipes.remove(<xreliquary:mob_ingredient:5>);
recipes.remove(<xreliquary:salamander_eye>);
recipes.remove(<xreliquary:witherless_rose>);
recipes.remove(<xreliquary:mob_ingredient:4>);
recipes.remove(<minecraft:skull:1>);
recipes.remove(<totemic:ceremony_cheat>);
recipes.remove(<minecraft:experience_bottle>);
recipes.remove(<botania:manaresource:5>);
recipes.remove(<botania:divacharm>);
recipes.remove(<xreliquary:harvest_rod>);
recipes.remove(<projectex:colossal_star_omega>);
recipes.remove(<roost:chicken>.withTag({Growth: 1, Chicken: "morechickens:funwaychick", Gain: 1, Strength: 1}));
recipes.remove(<draconicevolution:info_tablet>);
recipes.remove(<draconicevolution:chaos_shard:1>);
recipes.remove(<draconicevolution:chaos_shard:2>);
recipes.remove(<draconicevolution:chaos_shard:3>);
recipes.remove(<draconicevolution:chaos_shard:0>);
recipes.remove(<draconicevolution:celestial_manipulator>);
recipes.remove(<extrautils2:chunkloader>);
recipes.remove(<equivalentintegrations:transmutation_generator>);
recipes.remove(<equivalentintegrations:transmutation_chamber>);


