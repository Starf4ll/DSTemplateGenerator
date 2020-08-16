//////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////// Dungeon Siege Template Generator by Starfall //////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////
//																								//
////////////////////////////////////////// DESCRIPTION ///////////////////////////////////////////
//																								//
//	This program is designed to auto-generate Templates for Dungeon Siege 1 by reading the		//
//		raw data from templateUpload.csv and converting it to the proper format for Templates.	//
//																								//
//	Currently the program is capable of generating all types of armor and weapons and also		//
//		includes support for mixed stat requirements on armor (such as Strength + Dexterity).	//
//																								//
//	Damage, Defense, as well as Modifier Min and Max values will all be auto-calculated based	//
//		on the Equip Requirements and the type of template generated. Values will not be 		//
//		exactly the same as vanilla but follow a similar curve.									//
//																								//
//	It's recommended that you be familiar with SU 201 (Templates) and SU 211 (Naming Key)		//
//		before attempting to use this program.													//
//																								//
/////////////////////////////////////////// HOW TO USE ///////////////////////////////////////////
//																								//
//	The included file templateUpload.csv must be filled out before running the generator.		//
//	The file comes with several examples that can be used as a reference to get started.		//
//																								//
//	Instead of generating an entire template, you can also create variants which will			//
//	inherit the properties of the base template, with different equip requirements,				//
//	damage/defense values, models/textures, as well as inventory icons.							//
//																								//
//			Any fields that have a * next to them are REQUIRED for armor templates				//
//			Any fields that have a ^ next to them are REQUIRED for weapon templates				//
//			Any fields that have a % next to them are REQUIRED for armor variants				//
//			Any fields that have a $ next to them are REQUIRED for weapon variants				//
//		Any fields that have a & next to them are REQUIRED for shields (including variants)		//
//																								//
//----------------------------------------------------------------------------------------------//
//																								//
//	TEMPLATE NAME * ^ % $ &: This row should contain the name of the template. In order for the	//
//		generator to function properly, a specific format is expected for the name. The format	//
//		also helps ensure Dungeon Siege recognizes the template correctly for pcontent			//
//																								//
// ! ! ! ! ! !IT IS VERY IMPORTANT TO FOLLOW THE FORMAT, OR THE PROGRAM MAY NOT WORK! ! ! ! ! ! //
//																								//
//		General Weapon Format: {category}_g_c_{material}_{length}_{rarity}_{other info}			//
//																								//
//			Categories:																			//
//				ax	(Axes)																		//
//				bw	(Bows)																		//
//				cb	(Clubs)																		//
//				cw	(Crossbows)																	//
//				dg	(Daggers)																	//
//				hm	(Hammers)																	//
//				mc	(Maces)																		//
//				sd	(Swords)																	//
//				st	(Staves)																	//
//																								//
//			Materials:																			//
//				Optional: Can be anything or not included, just don't use the same letters as 	//
//				other parts of the name. Example: _st_ = Steel									//
//																								//
//			Lengths:																			//
//				s	(Short - For Bows only)														//
//				m	(Medium - For Bows and Crossbows only)										//
//				l	(Long - For Bows and Crossbows only)										//
//				1h	(Two-Handed - For melee weapons only)										//
//				2h	(Two-Handed - For melee weapons only)										//
//																								//
//			Rarities:																			//
//				Optional: Use one of the following or don't include for common rarity			//
//																								//
//				ra	(Rare)																		//
//				un	(Unique)																	//
//																								//
//			Other Info:																			//
//				Optional: You can put anything here to uniquely identify the template, but		//
//				again don't use the same letters as other parts of the name						//
//																								//
//																								//
//		General Armor Format: {category}_{material}_{class}_g_c_{rarity}_{mixstat}_{other info}	//
//																								//
//			Categories:																			//
//				bd	(Body/Chestpieces)															//
//				bo	(Boots)																		//
//				gl	(Gloves)																	//
//				he	(Helmets)																	//
//				sh	(Shields)																	//
//																								//
//			Materials:																			//
//				If you don't use one of the below options, generator will assume cloth to		//
//				determine body armor specialization												//
//																								//
//				br = Brigandine																	//
//				ba = Banded																		//
//				pl = Plate																		//
//				fp = Full Plate																	//
//				bp = Battle Plate																//
//				ch = Chain																		//
//				sc = Scale																		//
//				bl = Boiled Leather																//
//				le = Leather																	//
//				sl = Studded Leather															//
//				cl = Cloth																		//
//				ro = Robe																		//
//																								//
//			Classes:																			//
//				f	(Fighter - For STR items)													//
//				r	(Ranger - For DEX items)													//
//				m	(Mage - For INT items)														//
//																								//
//			Rarities:																			//
//				Optional: Use one of the following or don't include for common rarity			//
//																								//
//				ra	(Rare)																		//
//				un	(Unique)																	//
//																								//
//			Mixed Stats:																		//
//				Optional: You can include one of the below options to have the generator		//
//				use a mixture of stats (such as Strength and Dexterity). The stat requirements	//
//				and final defense will be use 60% of the first stat and 40% of the second.		//
//																								//
//				strdex																			//
//				strint																			//
//				dexstr																			//
//				dexint																			//
//				intstr																			//
//				intdex																			//
//																								//
//			Other Info:																			//
//				Optional: You can put anything here to uniquely identify the template, but		//
//				again don't use the same letters as other parts of the name						//
//																								//
//																								//
//		Variants Format: {variant}_{rarity}														//
//																								//
//			Variants:																			//
//				c_fin																			//
//				c_str																			//
//				c_mag																			//
//				c_sup																			//
//				o_avg																			//
//				o_fin																			//
//				o_str																			//
//				o_mag																			//
//				o_sup																			//
//																								//
//			Rarities:																			//
//				Optional: Use one of the following or don't include for common rarity			//
//																								//
//				ra	(Rare)																		//
//				un	(Unique)																	//
//																								//
//----------------------------------------------------------------------------------------------//
//																								//
//	SCREEN NAME * ^ &: This row defines what will show up as the name in-game as well as how	//
//		it will show up in Siege Editor. You can put anything in this field.					//
//																								//
//----------------------------------------------------------------------------------------------//
//																								//
//	MODEL ^ &: Defines what model the template will use in-game.								//
//																								//
//----------------------------------------------------------------------------------------------//
//																								//
//	TEXTURE: Defines what texture will be applied to the model of weapons and shields. Leaving	//
//		blank will mean the template can just use the default texture of the model.				//
//																								//
//----------------------------------------------------------------------------------------------//
//																								//
//	ARMOR TYPE *: Defines what model to use for armor.											//
//																								//
//----------------------------------------------------------------------------------------------//
//																								//
//	ARMOR STYLE *: Defines the texture to use for an armor's model.								//
//																								//
//----------------------------------------------------------------------------------------------//
//																								//
//	ACTIVE ICON: Defines what icon to show next to the character's portrait when the weapon		//
//		is equipped. Leaving blank will use the default icon for the weapon category.			//
//																								//
//----------------------------------------------------------------------------------------------//
//																								//
//	INVETORY ICON * ^ % $ &: Defines what icon to display in the character's inventory for the	//
//		item. If you leave this blank for some reason it will use b_gui_ig_i_it_skull-01		//
//																								//
//----------------------------------------------------------------------------------------------//
//																								//
//	INV HEIGHT: How many inventory spaces does the item take up vertically? If left blank the	//
//		item will use the default amount for the category										//
//																								//
//----------------------------------------------------------------------------------------------//
//																								//
//	INV WIDTH: How many inventory spaces does the item take up horizontally? If left blank the	//
//		item will use the default amount for the category										//
//																								//
//----------------------------------------------------------------------------------------------//
//																								//
//	REQUIREMENT: What is the stat requirement in order to equip this item? You don't need to	//
//		specify STR/DEX/INT, that is determined by the template name. If left blank the item	//
//		will have no requirement.																//
//																								//
//////////////////////////////////////////////////////////////////////////////////////////////////
