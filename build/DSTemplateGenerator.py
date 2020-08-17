# Import Python CSV and Math libraries and open our results file
import csv
import math
file_result = open('results.txt', 'w')

# Define the Class for our templates
class Template:
    def __init__(self, tname, sname, model, texture, atype, astyle,
                 inva, invi, invh, invw, category, rarity, stat, req, variant):
        self.tname = tname
        self.sname = sname
        self.model = model
        self.texture = texture
        self.atype = atype
        self.astyle = astyle
        self.inva = inva
        self.invi = invi
        self.invh = invh
        self.invw = invw
        self.category = category
        self.rarity = rarity
        self.stat = stat
        self.req = req
        self.variant = variant


# Determine specialization and category for template
def specializes(tn):
    print('BEGIN ' + tn)
    if tn[0:2] == 'bd':
        templates[i].category = 'body'
        if '_br_' in tn or '_ba_' in tn or '_pl_' in tn or '_fp_' in tn or '_bp_' in tn:
            return 'base_body_armor_plate'
        elif '_ch_' in tn or '_sc_' in tn:
            return 'base_body_armor_chain'
        elif '_bl_' in tn or '_le_' in tn or '_sl_' in tn:
            return 'base_body_armor_leather'
        else:
            return 'base_body_armor_cloth'
    elif tn[0:2] == 'gl':
        templates[i].category = 'glove'
        return 'base_glove'
    elif tn[0:2] == 'bo':
        templates[i].category = 'boot'
        return 'base_boot'
    elif tn[0:2] == 'he':
        templates[i].category = 'helm'
        return 'base_helm'
    elif tn[0:2] == 'sh':
        templates[i].category = 'shield'
        return 'base_shield'
    elif tn[0:2] == 'ax':
        templates[i].category = 'axe'
        templates[i].stat = 'strength'
        return 'base_axe'
    elif tn[0:2] == 'bw':
        templates[i].category = 'bow'
        templates[i].stat = 'dexterity'
        return 'base_bow'
    elif tn[0:2] == 'cb':
        templates[i].category = 'club'
        templates[i].stat = 'strength'
        return 'base_club'
    elif tn[0:2] == 'dg':
        templates[i].category = 'dagger'
        templates[i].stat = 'strength'
        return 'base_dagger'
    elif tn[0:2] == 'hm':
        templates[i].category = 'hammer'
        templates[i].stat = 'strength'
        return 'base_hammer'
    elif tn[0:2] == 'mc':
        templates[i].category = 'mace'
        templates[i].stat = 'strength'
        return 'base_mace'
    elif tn[0:2] == 'cw':
        templates[i].category = 'crossbow'
        templates[i].stat = 'dexterity'
        return 'base_projectile'
    elif tn[0:2] == 'st':
        templates[i].category = 'staff'
        templates[i].stat = 'intelligence'
        return 'base_staff'
    elif tn[0:2] == 'sd':
        templates[i].category = 'sword'
        templates[i].stat = 'strength'
        return 'base_sword'
    else:
        print('  CATEGORY NOT FOUND FOR {0}, DEFAULTING TO BODY'.format(str(templates[i].tname)))
        templates[i].category = 'body'


# Do we have an Aspect block? If so, what parameters?
def aspect_block(category):
    hasaspect = {'shield', 'axe', 'bow', 'club', 'dagger', 'hammer', 'mace', 'crossbow', 'staff', 'sword'}
    if category in hasaspect:
        if category == 'crossbow':          # Crossbows need a special Voice block
            if templates[i].texture == '':
                return str('[aspect]\n\t{{\n\t\tmodel = {0};\n\t\t[voice]\n\t\t{{\n\t\t\t[put_down]'
                           '\n\t\t\t{{\n\t\t\t\t* = s_e_gui_put_down_bow;\n\t\t\t}}\n\t\t}}\n\t}}\n\t'.format(
                                                                                            str(templates[i].model),))
            else:
                return str('[aspect]\n\t{{\n\t\tmodel = {0};\n\t\t[textures]\n\t\t'
                           '{{\n\t\t\t0 = {1};\n\t\t}}\n\t\t[voice]\n\t\t{{\n\t\t\t[put_down]'
                           '\n\t\t\t{{\n\t\t\t\t* = s_e_gui_put_down_bow;\n\t\t\t}}\n\t\t}}\n\t}}\n\t'.format(
                                                                    str(templates[i].model), str(templates[i].texture)))
        else:
            if templates[i].texture == '':
                return str('[aspect]\n\t{{\n\t\tmodel = {0};\n\t}}\n\t'.format(str(templates[i].model),))
            else:
                return str('[aspect]\n\t{{\n\t\tmodel = {0};\n\t\t[textures]\n\t\t'
                           '{{\n\t\t\t0 = {1};\n\t\t}}\n\t}}\n\t'.format(str(templates[i].model),
                                                                         str(templates[i].texture)))
    else:
        return ''


# Do we have an Attack block? If so, what parameters?
def attack_block(category):
    weapons = {'axe', 'bow', 'club', 'dagger', 'hammer', 'mace', 'crossbow', 'staff', 'sword'}
    shortweps = {'axe', 'dagger', 'hammer', 'mace'}
    if category in weapons:                 # Is this a weapon?
        if category in shortweps:           # Is this a short-range melee weapon?
            return str('[attack]\n\t{{\n\t\tattack_range = 0.5;\n\t{0}\n\t}}\n\t'.format(
                calc_attack(templates[i].tname, templates[i].category, templates[i].rarity, int(templates[i].req))))
        else:
            return str('[attack]\n\t{{\n\t{0}\n\t}}\n\t'.format(
                calc_attack(templates[i].tname, templates[i].category, templates[i].rarity, int(templates[i].req))))
    else:                                   # If not, must be armor
        return ''


# Calculate our damage
def calc_attack(tn, category, rarity, req):
    if templates[i].variant:                # Variants don't include weapon length, so we need to grab it from the
        tn = templates[i-1].tname           # previous template's name
    two_handed = False
    a_range = 0
    reload_delay = 0
    if rarity == 'common':                  # Common
        xmax = 3
        ymax = 15
        xmin = 2.4
        ymin = 10
    else:                                   # Rare or Unique
        xmax = 3.3
        ymax = 16
        xmin = 2.7
        ymin = 11
    if '2h' in tn:                          # Two-handed melee weapon
        offset = 1.75
        two_handed = True
    elif category == 'bow':
        if '_s_' in tn:                     # Short Bow
            reload_delay = 0
            a_range = 10
        elif '_m_' in tn:                   # Medium Bow
            reload_delay = 0.15
            a_range = 12
        else:                               # Long Bow
            reload_delay = 0.3
            a_range = 13
        offset = (1 + reload_delay)
    elif category == 'crossbow':
        if '_m_' in tn:                     # Medium Crossbow
            reload_delay = 0.5
            a_range = 13
        else:                               # Long Crossbow
            reload_delay = 0.7
            a_range = 15
        offset = (0.125 + reload_delay)
    elif category == 'staff':               # Staff
        offset = 1.4
        two_handed = True
    else:                                   # If none of the above, must be 1H Melee
        offset = 1
    dmax = offset * (((xmax * req * math.log(req, 10)) - (0.7 * req)) - ymax)
    dmin = offset * (((xmin * req * math.log(req, 10)) - (0.7 * req)) - ymin)
    if not templates[i].variant:            # Is this a variant?
        if two_handed:                      # Include line for Two Handed weapons
            return '  f damage_max = {0}.000000;\n\t  f damage_min = {1}.000000;\n\t\tis_two_handed = true;'.format(
                str(int(dmax)), str(int(dmin)))
        elif a_range != 0:                  # Is this a ranged weapon?
            if category == 'crossbow':      # Include line for ammo, range and reload delay for Crossbows
                return '\tammo_template = bolt;\n\t\tattack_range = {0};\n\t  f damage_max = {1}.000000;' \
                       '\n\t  f damage_min = {2}.000000;\n\t\treload_delay = {3};'.format(str(a_range), str(int(dmax)),
                                                                                   str(int(dmin)), str(reload_delay))
            else:                           # Include line for range and reload delay for Bows
                return '\tattack_range = {0};\n\t  f damage_max = {1}.000000;' \
                       '\n\t  f damage_min = {2}.000000;\n\t\treload_delay = {3};'.format(str(a_range), str(int(dmax)),
                                                                                   str(int(dmin)), str(reload_delay))
        else:                               # Must be a one handed melee weapon, just return the damage
            return '  f damage_max = {0}.000000;\n\t  f damage_min = {1}.000000;'.format(str(int(dmax)), str(int(dmin)))
    else:                                   # Variants should only return damage
        return '  f damage_max = {0}.000000;\n\t\t  f damage_min = {1}.000000;'.format(str(int(dmax)), str(int(dmin)))


# Determine if common/rare/unique and also return screen name
def common_block(current_template, screen_name):
    if '_ra_' in current_template or '_ra]' in current_template:
        templates[i].rarity = 'rare'
        return 'pcontent_special_type = rare;\n\t\tscreen_name = \"{0}\"'.format(str(screen_name))
    elif '_un_' in current_template or '_un]' in current_template:
        templates[i].rarity = 'unique'
        return 'pcontent_special_type = unique;\n\t\tscreen_name = \"{0}\"'.format(str(screen_name))
    else:
        templates[i].rarity = 'common'
        return 'screen_name = \"{0}\"'.format(str(screen_name))


# Do we have a Defense block? If so, what parameters?
def defense_block(category):
    weapons = {'axe', 'bow', 'club', 'dagger', 'hammer', 'mace', 'crossbow', 'staff', 'sword'}
    if category in weapons:                 # Is this a weapon?
        return ''
    else:                                   # If not, must be armor
        stat_type(templates[i].tname)       # Determine stat type before proceeding
        if category == 'shield':
            return '[defend]\n\t{{\n\t  f defense = {0}.000000;\n\t}}\n\t'.format(str(
                int(calc_defense(templates[i].stat, templates[i].category, templates[i].rarity))))
        elif category == 'body' or 'glove' or 'boot' or 'helm':
            return '[defend]\n\t{{\n\t\tarmor_style = {0};\n\t\tarmor_type = {1};\n\t  f defense = {2}.000000;\n\t' \
                   '}}\n\t'.format(str(templates[i].astyle), str(templates[i].atype),
                                   str(int(calc_defense(templates[i].stat,
                                                        templates[i].category, templates[i].rarity))))


# What stat type is being used for our armor?
def stat_type(current_template):
    if '_strdex_' in current_template:
        templates[i].stat = 'strdex'
    elif '_strint_' in current_template:
        templates[i].stat = 'strint'
    elif '_dexstr_' in current_template:
        templates[i].stat = 'dexstr'
    elif '_dexint_' in current_template:
        templates[i].stat = 'dexint'
    elif '_intstr_' in current_template:
        templates[i].stat = 'intstr'
    elif '_intdex_' in current_template:
        templates[i].stat = 'intdex'
    elif '_f_' in current_template:
        templates[i].stat = 'strength'
    elif '_r_' in current_template:
        templates[i].stat = 'dexterity'
    elif '_m_' in current_template:
        templates[i].stat = 'intelligence'
    else:
        print(' STAT TYPE NOT FOUND FOR {0}, DEFAULTING TO STRENGTH'.format(str(templates[i].tname)))
        templates[i].stat = 'strength'


# Calculate our defense
def calc_defense(stat, category, rarity):
    if category == 'body':                   # Body armor
        if rarity == 'common':
            exponent = .35
            modifier = 4.2
        else:
            exponent = .38
            modifier = 4.4
    elif category == 'glove':                # Gloves
        if rarity == 'common':
            exponent = .15
            modifier = -1.15
        else:
            exponent = .16
            modifier = -1.1
    elif category == 'boot':                # Boots
        if rarity == 'common':
            exponent = .16
            modifier = -1.1
        else:
            exponent = .17
            modifier = -1.05
    elif category == 'helm':                # Helmets
        if rarity == 'common':
            exponent = .17
            modifier = -1.05
        else:
            exponent = .18
            modifier = -1.0
    else:                                   # If none of the above, must be a shield
        if rarity == 'common':
            exponent = .21
            modifier = -1.0
        else:
            exponent = .225
            modifier = -1.0
    if templates[i].req == '':
        print('   NO EQUIP REQUIREMENT SPECIFIED FOR {0}, DEFAULTING TO 10'.format(str(templates[i].tname)))
        templates[i].req = '10'
    n = int(templates[i].req) * ((int(templates[i].req) ** exponent) + modifier)
    if stat == 'strength':
        return n
    elif stat == 'dexterity':
        final_defense = int(n * 0.75)
        return final_defense
    elif stat == 'intelligence':
        final_defense = int(n * 0.5)
        return final_defense
    elif stat == 'strdex':
        final_defense = int((n * 0.6) + (n * 0.4 * 0.75))
        return final_defense
    elif stat == 'strint':
        final_defense = int((n * 0.6) + (n * 0.4 * 0.5))
        return final_defense
    elif stat == 'dexstr':
        final_defense = int((n * 0.6 * 0.75) + (n * 0.4))
        return final_defense
    elif stat == 'dexint':
        final_defense = int((n * 0.6 * 0.75) + (n * 0.4 * 0.5))
        return final_defense
    elif stat == 'intstr':
        final_defense = int((n * 0.6 * 0.5) + (n * 0.4))
        return final_defense
    else:
        final_defense = int((n * 0.6 * 0.5) + (n * 0.4 * 0.75))
        return final_defense


# What's in our GUI Block?
def gui_block():
    if templates[i].invi == '':
        print('    INVENTORY ICON NOT FOUND FOR {0}, DEFAULTING TO A SKULL'.format(str(templates[i].tname)))
        templates[i].invi = 'b_gui_ig_i_it_skull-01'
    if templates[i].inva == '':
        return '[gui]\n\t{{\n\t\t{0}{1}inventory_icon = {2};\n\t}}\n\t'.format(
            eq_reqs(templates[i].stat, templates[i].req), inv_size(), str(templates[i].invi))
    else:
        return '[gui]\n\t{{\n\t\t{0}{1}active_icon = {2};\n\t\tinventory_icon = {3};\n\t}}\n\t'.format(
            eq_reqs(templates[i].stat, templates[i].req), inv_size(), str(templates[i].inva), str(templates[i].invi))


# What do we return for the equip requirements in the GUI Block?
def eq_reqs(stat, req):
    if req == '10' or req == '':
        return ''
    else:
        req = int(req)
        reqs = [str(int((req / 0.7) * 0.6)), str(int((req / 0.7) * 0.4)), str(req)]
        if stat == 'strength' or stat == 'dexterity' or stat == 'intelligence':
            return 'equip_requirements = {0}:{1};\n\t\t'.format(stat, req)
        elif stat == 'strdex':
            return 'equip_requirements = strength:{0},dexterity:{1}; // Equivalent to stat LV {2}\n\t\t'.format(
                reqs[0], reqs[1], reqs[2])
        elif stat == 'strint':
            return 'equip_requirements = strength:{0},intelligence:{1}; // Equivalent to stat LV {2}\n\t\t'.format(
                reqs[0], reqs[1], reqs[2])
        elif stat == 'dexstr':
            return 'equip_requirements = dexterity:{0},strength:{1}; // Equivalent to stat LV {2}\n\t\t'.format(
                reqs[0], reqs[1], reqs[2])
        elif stat == 'dexint':
            return 'equip_requirements = dexterity:{0},intelligence:{1}; // Equivalent to stat LV {2}\n\t\t'.format(
                reqs[0], reqs[1], reqs[2])
        elif stat == 'intstr':
            return 'equip_requirements = intelligence:{0},strength:{1}; // Equivalent to stat LV {2}\n\t\t'.format(
                reqs[0], reqs[1], reqs[2])
        elif stat == 'intdex':
            return 'equip_requirements = intelligence:{0},dexterity:{1}; // Equivalent to stat LV {2}\n\t\t'.format(
                reqs[0], reqs[1], reqs[2])


# What do we return for inventory height/width in the GUI Block?
def inv_size():
    if templates[i].invh != '' and templates[i].invw != '':
        return 'inventory_height = {0};\n\t\tinventory_width = {1};\n\t\t'.format(str(templates[i].invh),
                                                                                  str(templates[i].invw))
    elif templates[i].invh != '':
        return 'inventory_height = {0};\n\t\t'.format(str(templates[i].invh))
    elif templates[i].invw != '':
        return 'inventory_width = {0};\n\t\t'.format(str(templates[i].invw))
    else:
        return ''


# Calculate our modifiers
def calc_mods(category, rarity):
    weapons = {'axe', 'bow', 'club', 'dagger', 'hammer', 'mace', 'crossbow', 'staff', 'sword'}
    if category in weapons:                 # Is this a weapon?
        if rarity == 'common':
            mod_max_mult = 1.0
            mod_min_mult = 0.15
        else:
            mod_max_mult = 1.2
            mod_min_mult = 0.33
    else:                                   # If not, must be armor
        if rarity == 'common':
            mod_max_mult = 0.8
            mod_min_mult = 0.1
        else:
            mod_max_mult = 1.0
            mod_min_mult = 0.25
    return '  f modifier_max = {0}.000000;\n\t\t  f modifier_min = {1}.000000;\n\t\t'.format(
        str(int(int(templates[i].req) * mod_max_mult)),
        str(int(int(templates[i].req) * mod_min_mult)))


# Is this a variant?
def is_variant(vn):
    variants = {'c_fin', 'c_str', 'c_mag', 'c_sup', 'o_avg', 'o_fin', 'o_str', 'o_mag', 'o_sup'}
    if 'ra' in vn:
        templates[i].rarity = 'rare'
    elif 'un' in vn:
        templates[i].rarity = 'unique'
    else:
        templates[i].rarity = 'common'
    if vn[0:5] in variants:
        print('BEGIN ' + vn)
        print(' TEMPLATE IS A VARIANT, USING PREVIOUS TEMPLATE\'S CATEGORY AND STAT TYPE')
        templates[i].category = templates[i - 1].category
        templates[i].stat = templates[i - 1].stat
        templates[i].variant = True
        return True
    else:
        return False


# Handling for armor variants
def amr_variant(category):
    if category == 'shield':
        return 'model = {0};\n\t\t\ttexture = {1};\n\t\t\t{2}\tinventory_icon = {3};\n\t\t' \
               '  f defense = {4}.000000;\n\t\t{5}{6}}}'.format(templates[i].model, templates[i].texture,
                               eq_reqs(templates[i].stat, templates[i].req), templates[i].invi,
                               str(int(calc_defense(templates[i].stat, templates[i].category, templates[i].rarity))),
                               calc_mods(templates[i].category, templates[i].rarity),
                               variant_rarity(templates[i].rarity))
    else:
        return 'armor_style = {0};\n\t\t\tarmor_type = {1};\n\t\t\t{2}\tinventory_icon = {3};\n\t\t' \
               '  f defense = {4}.000000;\n\t\t{5}{6}}}'.format(templates[i].astyle, templates[i].atype,
                               eq_reqs(templates[i].stat, templates[i].req), templates[i].invi,
                               str(int(calc_defense(templates[i].stat, templates[i].category, templates[i].rarity))),
                               calc_mods(templates[i].category, templates[i].rarity),
                               variant_rarity(templates[i].rarity))


# Handling for weapon variants
def wep_variant():
    if not templates[i].texture == '':      # Does our weapon have a texture?
        return 'model = {0};\n\t\t\ttexture = {1};\n\t\t\t{2}\tinventory_icon = {3};\n\t\t' \
               '{4}\n\t\t{5}{6}}}'.format(templates[i].model, templates[i].texture,
                              eq_reqs(templates[i].stat, templates[i].req), templates[i].invi,
                              str(calc_attack(templates[i].tname, templates[i].category, templates[i].rarity,
                              int(templates[i].req))), calc_mods(templates[i].category, templates[i].rarity),
                              variant_rarity(templates[i].rarity))
    else:                                   # If not, don't include a line for texture
        return 'model = {0};\n\t\t\t{1}\tinventory_icon = {2};\n\t\t' \
               '{3}\n\t\t{4}{5}}}'.format(templates[i].model, eq_reqs(templates[i].stat,
                              templates[i].req), templates[i].invi, str(calc_attack(templates[i].tname,
                              templates[i].category, templates[i].rarity, int(templates[i].req))),
                              calc_mods(templates[i].category, templates[i].rarity),
                              variant_rarity(templates[i].rarity))


# Variant Rarity
def variant_rarity(rarity):
    if rarity == 'common':
        return ''
    else:
        return '\tpcontent_special_type = {0};\n\t\t'.format(rarity)


# Create templates from CSV
templates = []
with open('templateUpload.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            templates.append(Template(row[0], row[1], row[2], row[3], row[4],
                                      row[5], row[6], row[7], row[8], row[9], '', '', '', row[10], False))
            line_count += 1

# Loop through all templates and write to file
for i in range(len(templates)):
    if not is_variant(templates[i].tname):  # Is this a variant?
        if i > 0:
            file_result.write('\n\t}\n}\n\n')
        file_result.write('[t:template,n:{0}]\n{{\n\tdoc = \"{1}\";\n\tspecializes = {2};\n\t{3}{4}[common]\n\t{{\n\t\t'
                          '{5};\n\t}}\n\t{6}{7}[pcontent]\n\t{{\n\t\t[base]\n\t\t{{\n\t\t{8}}}'.format(
                                str(templates[i].tname), str(templates[i].sname), specializes(templates[i].tname),
                                aspect_block(templates[i].category), attack_block(templates[i].category),
                                common_block(templates[i].tname, templates[i].sname),
                                defense_block(templates[i].category), gui_block(), calc_mods(templates[i].category,
                                templates[i].rarity)))
    else:
        armor = {'body', 'glove', 'boot', 'helm', 'shield'}
        if templates[i].category in armor:  # Is this an armor variant?
            file_result.write('\n\t\t[{0}]\n\t\t{{\n\t\t\t{1}'.format(templates[i].tname[0:5],
                                                                      amr_variant(templates[i].category)))
        else:                               # If not, must be a weapon variant
            file_result.write('\n\t\t[{0}]\n\t\t{{\n\t\t\t{1}'.format(templates[i].tname[0:5],
                                                                      wep_variant()))
file_result.write('\n\t}\n}')
print('ALL TEMPLATES COMPLETED')
