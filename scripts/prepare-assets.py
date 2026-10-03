"""Reproduce web assets from the local Marsfall art library. Originals stay intact."""
from pathlib import Path
import json, re, shutil
from PIL import Image

SITE = Path(__file__).resolve().parents[1]
SOURCE = SITE.parent
OUT = SITE / 'assets'
OUT.mkdir(exist_ok=True)
concept = SOURCE / 'Marsfall-v3/Concept-Art'

def slug(text):
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')

manifest = []
def image(source, name, size=1254, crop=None):
    im = Image.open(SOURCE / source).convert('RGB')
    if crop: im = im.crop(crop)
    im.thumbnail((size, size), Image.Resampling.LANCZOS)
    relative = f'assets/{name}.webp'
    im.save(SITE / relative, 'WEBP', quality=86, method=6)
    manifest.append({'output':relative, 'source':source, 'crop':crop, 'width':im.width, 'height':im.height, 'bytes':(SITE / relative).stat().st_size})
    return relative

# Roles and descriptions follow frontier.gd / campaign.gd. Keep this editorial,
# rather than publishing balancing values which change between game builds.
descriptions = {
 'Infantry':('Rifle infantry','The backbone of the Ares front line. Versatile rifle soldiers punish exposed rocket troops. Spread them out when enemy grenadiers arrive.'),
 'Grenadier':('Anti-infantry','Break up tightly packed infantry with explosive splash damage. Keep these specialists away from enemy armor and fast raiders.'),
 'Bazooka':('Anti-armor','Long-reaching rockets make this soldier a dangerous answer to heavy vehicles. Screen your launchers with rifle infantry and punish unsupported tanks.'),
 'Commando':('Elite assault','A fast, durable assault specialist for an aggressive advance. Push into vulnerable positions with the rest of your force close behind.'),
 'Sniper':('Long-range precision','A precision rifle rewards careful positioning and clear sightlines. Keep a screen of friendly units nearby: close attackers can overwhelm a sniper.'),
 'Suicide Bomber':('Explosive assault','A volatile contact attacker that trades its own survival for a damaging blast. Timing and approach matter more than staying power.'),
 'Engineer':('Mission specialist','Captures mission technology. Escort this unarmed specialist to the objective and keep hostile fire away from the capture operation.'),
 'Hero':('Faction commander','Commander Vale combines improved armor with a powerful weapon. Lead from the front, or take direct control when the mission calls for a personal touch.'),
 'Drone':('Aerial reconnaissance','An inexpensive, unarmed flying scout with extended vision. Reveal the battlefield, watch enemy approaches, and gather information before committing your army.'),
 'Jeep':('Fast scout & raider','The Trailblazer Jeep races ahead of the army to scout and raid. Hunt exposed harvesters and grenadiers, then pull back before rifles and rockets close in.'),
 'Rover':('Armored escort','A mobile infantry escort with more staying power than the Jeep. Its independent turret covers an advance, but enemy anti-armor weapons remain a serious threat.'),
 'Tank':('Heavy frontline armor','A slow, armored hovertank built to anchor an advance and crush infantry. Combine it with supporting soldiers to answer long-range rocket teams.'),
 'Harvester':('Crystal economy','An unarmed crystal truck keeps your economy moving. Protect the route between your crystal fields and base: a stranded harvester can stall an offensive.'),
 'Rocket Launcher':('Long-range artillery','A mobile platform for long-range splash rockets. Position it behind your front line and let your scouts reveal worthwhile targets.'),
 'Mine Layer':('Area denial','Lays proximity mines while moving and attacking. Shape the enemy approach and make exposed routes dangerous before the main force arrives.'),
 'Missile Ship':('Naval fire support','A long-range naval missile platform produced at a coastal Shipyard. Strike inland targets from the water and watch the skies for Xenaari predators.'),
 'Command Hub':('Command & economy','The center of your foothold on Mars. Anchor your expansion, field reconnaissance drones, and keep this critical structure protected.'),
 'Power Plant':('Energy production','Supplies the power your growing base needs. Expand your energy network alongside production and defense so the next building is ready when you need it.'),
 'Barracks':('Infantry production','Recruit the soldiers that hold the line. Build rifle, grenade, and rocket teams around the threats on the battlefield.'),
 'Factory':('Vehicle production','Turn a foothold into an armored force. Produce combat vehicles and combine speed, protection, and fire support in your next push.'),
 'Repair Bay':('Vehicle support','Repairs nearby vehicles and trucks. A protected repair position gives damaged armor a route back into the fight.'),
 'Hospital':('Infantry support','Heals nearby soldiers. Place it where returning squads can recover without exposing the building to an enemy advance.'),
 'Crystal Farm':('Resource production','Establish a crystal supply with an automatic harvesting truck. Defend the deposit and its approach to keep your production queues moving.'),
 'Food Farm':('Army evolution','Nearby units receive periodic upgrades, up to three improvements. Give your force time to grow stronger before committing to the next battle.'),
 'Watchtower':('Garrison defense','An elevated defensive position for up to three soldiers. Occupy it with your chosen infantry and unload them when the front line moves.'),
 'Turret':('Rapid-fire defense','An autonomous rapid-fire weapon that guards your base. Cover vulnerable approaches and support friendly troops with sustained fire.'),
 'Laser':('Anti-vehicle defense','A powerful beam defense specialized against vehicles. Protect its position with infantry and other defenses to stop a mixed enemy force.'),
 'Orbital Energy Array':('Strategic superweapon','A charged strategic weapon for decisive strikes. Protect it while it prepares, then choose the target that changes the battle.'),
 'Hologram Decoy':('Tactical deception','A fragile hologram that lures alien attackers. Draw attention away from a vulnerable position and give your real force room to act.'),
 'Shield Generator':('Base protection','Reduces damage to nearby friendly structures. Place it inside a cluster of valuable buildings to strengthen the core of your base.'),
 'Shipyard':('Naval production','A shoreline production facility for missile ships. Expand toward the water and open a new angle on the enemy position.'),
 'Stalker':('Brood infantry','The Xenaari answer to a rifle line: agile frontline infantry for the living army. Use numbers and support to close down vulnerable enemy specialists.'),
 'Spitter':('Anti-infantry','An organic counterpart to the grenadier. Its attacks punish groups of exposed soldiers; enemy vehicles demand support from heavier brood units.'),
 'Lanceborn':('Anti-armor','Heavy bio-weapon infantry that threaten human armor. Keep them behind a protective screen and bring their firepower to bear on enemy vehicles.'),
 'Brood Queen':('Faction commander','Broodmother Nyx leads the Xenaari defense of Mars. A durable commander with a powerful weapon, ready for direct control when the situation demands it.'),
 'Skimmer':('Fast scout & raider','A swift four-legged brood scout that fills the light-raider role. Probe the human perimeter and strike exposed economy units before retreating.'),
 'Behemoth':('Heavy siege beast','A massive armored creature that anchors the brood front line. Advance with supporting organisms to keep enemy rocket specialists from picking it apart.'),
 'Great Sandworm':('Burrowing assault','An enormous melee creature that can travel underground. Surface near vulnerable enemies and turn a quiet stretch of ground into a close-range threat.'),
 'Sky Manta':('Flying bio-craft','A slow, flying brood craft. Take direct control to rise and descend, or use it as part of a combined force above the ground battle.'),
 'Sky Reaver':('Anti-naval predator','A flying alien creature particularly dangerous to ships. Keep pressure on the water and punish human naval forces left without support.'),
 'Kamikaze':('Explosive assault','A fast brood attacker that detonates on contact with explosive splash damage. A well-timed approach can punish an exposed enemy group.'),
 'Brood Nexus':('Brood command','The living heart of the Xenaari base. Protect the Nexus while the brood expands across the Martian landscape.'),
 'Plasma Well':('Living energy reactor','Powers the organic base. Keep enough living reactors protected to sustain the next wave of brood production and defenses.'),
 'Hatchery':('Infantry spawning','The spawning ground for the brood infantry line. Field Stalkers, Spitters, and Lanceborn to match the human force at your perimeter.'),
 'Morph Foundry':('Creature production','A production den for larger combat organisms. Bring heavy beasts and specialized creatures into the battle as your base develops.'),
 'Mending Pool':('Heavy-unit support','Restores nearby heavy units. Pull damaged creatures back toward the pool and keep their support position protected.'),
 'Regrowth Sanctuary':('Infantry recovery','Heals nearby brood infantry. Give your surviving organisms a sheltered place to recover between battles.'),
 'Evolution Garden':('Brood evolution','Periodically improves nearby units, up to three upgrades. Build a stronger brood before sending it into the next engagement.'),
 'Breeding Ground':('Passive crystal income','Generates alien resources automatically. The brood builds its economy around protected living structures instead of harvesting trucks.'),
 'Sentinel Spire':('Brood garrison','A tall living defensive position that can hold up to three infantry units. Guard approaches and unload its occupants when you need them in the field.'),
 'Spore Battery':('Organic rapid fire','An autonomous organic defense with rapid-fire attacks. Support the brood perimeter with overlapping fields of fire.'),
 'Void Lance':('Anti-vehicle defense','A living beam weapon that specializes against enemy vehicles. Guard it against infantry while it threatens advancing human armor.'),
 'Locust Hive':('Strategic superweapon','The brood’s charged strategic weapon. Protect the Hive through its preparation, then unleash it against a carefully chosen enemy position.'),
 'Critter':('Martian wildlife','A small roaming inhabitant of the Martian wilds. The battlefield belongs to more than the two armies fighting over it.'),
 'Titan':('Massive hostile wildlife','A towering native threat with the strength to disrupt an entire front line. Keep your army ready for a danger that does not wear either faction’s colors.'),
 'Collector':('Mission resource carrier','A Xenaari resource carrier used in specific resource-race missions. Its mission role differs from the brood’s normal passive crystal economy.'),
 'Crystal Assimilator':('Mission economy structure','An alien resource structure used in specific resource-race missions. The normal brood economy relies on Breeding Grounds instead.'),
 'Relay':('Mission structure','A communications structure encountered in mission objectives. Follow the briefing to learn which positions must be secured or defended.'),
 'Terminal':('Mission structure','A technology objective that places the mission’s capture and defense decisions on the map. Escort specialists and read the operation briefing.'),
 'Fortress':('Mission stronghold','A heavily protected objective structure in the campaign. Prepare a coordinated force and follow the operation’s victory conditions.'),
 'Caravan':('Mission transport','A protected transport in escort operations. Keep the route clear, guard it against enemy attacks, and guide it toward the mission destination.'),
 'Wreck':('Capturable vehicle wreck','A destroyed human vehicle can become a new threat. Xenaari units can occupy the wreck and turn it into an explosive attacker.'),
 'Command Core':('Enemy command objective','An enemy command structure that anchors a hostile foothold. Read your operation briefing and coordinate an attack on its defenses.'),
}
catalogue=[]
skip={'Hero-Gatling','Infantry-Blueprint','Critter-Field-Study','Creatures-Lands'}
for folder in sorted(concept.iterdir()):
    if folder.name=='Movie-Posters': continue
    for path in sorted(folder.glob('*.png')):
        name=re.sub(r'^Concept-(Ares|Xenaari|Roaming)-','',path.stem)
        if name in skip: continue
        name=name.replace('-',' ')
        faction='ares' if folder.name.startswith('Ares') else 'xenaari' if folder.name.startswith('Xenaari') else 'wildlife'
        kind='building' if 'Buildings' in folder.name else 'creature' if faction=='wildlife' else 'unit'
        ident=slug(f'{faction}-{name}')
        role,description=descriptions.get(name, ('', ''))
        assert role and description, name
        if faction=='xenaari' and name in ['Sniper','Commando','Suicide Bomber','Rocket Launcher','Mine Layer']:
            description=description.replace('soldier','organism').replace('rifle','bio-rifle')
        if faction=='xenaari' and name=='Shield Generator': description='A living shield defense that reduces damage to nearby friendly structures. Protect the center of your brood base with overlapping support.'
        catalogue.append({'id':ident,'name':{'Hero':'Commander Vale','Tank':'Hovertank','Jeep':'Trailblazer Jeep','Brood Queen':'Broodmother Nyx'}.get(name,name),'faction':faction,'kind':kind,'role':role,'description':description,'image':image(str(path.relative_to(SOURCE)).replace('\\','/'),ident), 'artType':'Concept art'})

def add(name,faction,kind,source,crop=None,mission=False):
    ident=slug(f'{faction}-{name}')
    role,desc=descriptions[name]
    catalogue.append({'id':ident,'name':name,'faction':faction,'kind':kind,'role':role,'description':desc,'image':image(source,ident,crop=crop),'artType':'Concept atlas detail' if crop else 'Concept art','mission':mission})

add('Barracks','ares','building','Marsfall-v3/Concept-Barracks.png')
add('Factory','ares','building','Marsfall-v2/art-direction/concepts/ares-factory-concept.png')
atlas='Marsfall-v2/art-direction/xenaari-complete-concept-atlas.png'
def brood_cell(col,row): return (8+col*168,88+row*191,172+col*168,88+row*191+151)
add('Hatchery','xenaari','building',atlas,brood_cell(2,3))
add('Morph Foundry','xenaari','building',atlas,brood_cell(3,3))
add('Collector','xenaari','unit',atlas,brood_cell(0,2),True)
add('Crystal Assimilator','xenaari','building',atlas,brood_cell(0,4),True)
for name,col in [('Relay',3),('Terminal',4),('Fortress',5)]:
    add(name,'xenaari','building',atlas,brood_cell(col,5),True)
# The campaign's human mission structures have their own atlas designs.
ares_atlas='Marsfall-v2/art-direction/ares-complete-concept-atlas.png'
for name,col,row in [('Relay',4,5),('Terminal',5,5),('Fortress',0,6)]:
    add(name,'ares','building',ares_atlas,(8+col*168,88+row*191,172+col*168,88+row*191+151),True)
for name,col,row,kind in [('Caravan',4,2,'unit'),('Wreck',5,2,'unit'),('Command Core',1,3,'building')]:
    add(name,'ares',kind,ares_atlas,(8+col*168,88+row*191,172+col*168,88+row*191+151),True)

gallery=[]
def gal(source,name,title,category,description):
    gallery.append({'id':name,'title':title,'category':category,'description':description,'image':image(source,name,1800)})

gal('Marsfall-v3/Concept-Art/Movie-Posters/Red-Frontier-Marsfall-Poster-Vale-vs-Titan-16x9.png','cover','Vale against the Titan','Concept art','Cinematic key art: Commander Vale faces a native Martian Titan.')
gal('Marsfall-v3/Concept-Art/Movie-Posters/Red-Frontier-Marsfall-Poster-Brood-Queen-16x9.png','brood-cover','The brood rises','Concept art','Cinematic key art for the Xenaari defense of Mars.')
gal('Marsfall-v3/Concept-Art/Movie-Posters/Red-Frontier-Marsfall-Poster-Ares-Bazooka-16x9.png','bazooka-cover','Hold the frontier','Concept art','Ares rocket infantry in a cinematic Martian battle scene.')
gal('Marsfall-v3/Concept-Art/Movie-Posters/Red-Frontier-Marsfall-Poster-Xenaari-Spitter-16x9.png','spitter-cover','Born for the battle','Concept art','A cinematic illustration of the Xenaari Spitter.')
for source,name,title,desc in [
 ('Marsfall-v3/assets/infantry/ares_pbr/AresInfantry_PBR_ThreeQuarter_Render.png','infantry-render','Ares infantry','The authored infantry model in a three-quarter material preview.'),
 ('Marsfall-v3/assets/models/Rover_Ares_PBR/Rover_Ares_Concept_PBR_Render.png','rover-render','Ares Rover','An authored Rover model with independent turret and detailed hull.'),
 ('Marsfall-v2/art-direction/blender/Tank.png','tank-render','The hovertank','Studio render of the armored Ares hovertank.'),
 ('Marsfall-v2/art-direction/blender/Barracks.png','barracks-render','An Ares foothold','Studio render of the Ares Barracks model.'),
 ('Marsfall-v2/art-direction/blender/Infantry.png','soldier-render','Rifle soldier','Studio render of the rifle infantry model.'),
 ('Marsfall-v2/art-direction/blender/Grenadier.png','grenadier-render','Grenadier','Studio render of the explosive infantry specialist.'),
 ('Marsfall-v2/art-direction/blender/Bazooka.png','bazooka-render','Rocket specialist','Studio render of the anti-armor soldier.'),
 ('Marsfall-v2/art-direction/blender/Trailblazer.png','jeep-render','Trailblazer Jeep','Studio render of the light Ares scout vehicle.'),
 ('work/buildings1/Godot-buildings.png','buildings-render','Build your front line','A rendered presentation of the Command Hub, Barracks, Factory, and turret.'),
 ('work/behemoth-source.png','behemoth-render','Xenaari Behemoth','Authored creature model preview from the Xenaari asset work.'),
 ('work/new-units/Spitter-source.png','spitter-render','The Spitter model','Authored Xenaari Spitter model preview.'),
 ('work/new-units/Skimmer-source.png','skimmer-render','The Skimmer model','Authored Xenaari Skimmer model preview.'),
]: gal(source,name,title,'Model renders',desc)
for source,name,title,desc in [
 ('Marsfall-v3/Remodel-first-person.png','direct-control','Take the front line','Gameplay capture from the direct-control view. The battle continues around your unit.'),
 ('Marsfall-v3/Immersion-Humans.png','ares-gameplay','Ares on the ground','Gameplay capture of an Ares force on Mars.'),
 ('Marsfall-v3/Immersion-Brood.png','brood-gameplay','Meet the brood','Gameplay capture of the Xenaari faction.'),
 ('Marsfall-v3/Immersion-Terrain.png','terrain-gameplay','Beyond the landing zone','Gameplay capture of a Martian battlefield.'),
 ('Marsfall-v3/work/Spitter-Last-Stand-gameplay.png','spitter-gameplay','A living army','Gameplay capture featuring the authored Xenaari Spitter.'),
 ('Marsfall-v3/work/survival-update/Last-Stand-base-and-dropship.png','last-stand','The Last Stand','Gameplay capture of the Last Stand operation, base, and dropship.'),
 ('Marsfall-v3/work/cantina-rebuild/cantina.png','cantina','Between battles','Gameplay capture inside the Martian cantina.'),
]: gal(source,name,title,'Gameplay',desc)
for source,name,title,desc in [
 ('Marsfall-v2/art-direction/ares-complete-concept-atlas.png','ares-atlas','Ares design archive','The full Ares concept atlas, including combat units, structures, and mission designs.'),
 ('Marsfall-v2/art-direction/xenaari-complete-concept-atlas.png','brood-atlas','Xenaari design archive','The full Xenaari concept atlas. Some designs are mission-specific or exploratory.'),
 ('Marsfall-v3/Concept-Art/Ares-Expedition-Units/Concept-Ares-Infantry-Blueprint.png','infantry-blueprint','Anatomy of a soldier','Concept blueprint of the Ares infantry armor.'),
 ('Marsfall-v3/Concept-Art/Ares-Expedition-Units/Concept-Ares-Hero-Gatling.png','vale-concept','Commander Vale: heavy weapon','An alternate concept study for the Ares commander.'),
 ('Marsfall-v3/Concept-Art/Roaming-Creatures/Concept-Roaming-Critter-Field-Study.png','critter-study','Martian field study','A concept study of Mars’s roaming native wildlife.'),
 ('Marsfall-v3/Concept-Art/Roaming-Creatures/Concept-Roaming-Creatures-Lands.png','wildlife-landscape','A world with teeth','Landscape concept art with Martian wildlife.'),
]: gal(source,name,title,'Concept art',desc)

fonts=OUT / 'fonts'
fonts.mkdir(exist_ok=True)
shutil.copy2(SOURCE / 'Marsfall-v3/assets/fonts/Rajdhani-SemiBold.ttf', fonts / 'Rajdhani-SemiBold.ttf')
shutil.copy2(SOURCE / 'Marsfall-v3/assets/fonts/OFL.txt', fonts / 'OFL.txt')
(SITE / 'src').mkdir(exist_ok=True)
(SITE / 'src/content.js').write_text('export const catalogue = '+json.dumps(catalogue,indent=2,ensure_ascii=False)+';\n\nexport const gallery = '+json.dumps(gallery,indent=2,ensure_ascii=False)+';\n',encoding='utf-8')
(SITE / 'asset-sources.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(f'{len(catalogue)} catalogue entries, {len(gallery)} gallery pieces, {len(manifest)} assets; {sum(m["bytes"] for m in manifest)/1024/1024:.1f} MB optimized')
