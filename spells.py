import sqlite3
import pandas as pd
import re
import discord
from discord.ext import commands

def displaySpell(spellName):
    conn = sqlite3.connect('DungeonsNDragons.db')
    conn.row_factory = sqlite3.Row
    # inputclass = "Wizard"
    # inputSpellName = "Polymorph"
    # spellName = spellName.replace("'","''")
    # if inputSpellName:
    #     table = conn.execute(f"select * from spells where spellClasses like '%{inputclass}%' and spellName = '{inputSpellName}' order by spellLevel,spellName")
    # else:
    #     table = conn.execute(f"select * from spells where spellClasses like '%{inputclass}%' order by spellLevel,spellName")
    spellName = spellName.title().replace("'S","'s")
    table = conn.execute("select * from spells where spellName like? LIMIT 1", (spellName,))
    # table = conn.execute(f"select * from spells where spellName = '{spellName.title()}' LIMIT 1")


    for row in table:
        ritualCaster = False
        # if table.rowcount == 1:
        formattedspellName = row['spellName'].title().replace("'S","'s")
        retVal = f"__**{formattedspellName}**__\n"

        if row['spellLevel'] == 0:
            spellLeveltext = 'Cantrip'
        elif row['spellLevel'] == 1:
            spellLeveltext = f"{row['spellLevel']}st-level"
        elif row['spellLevel'] == 2:
            spellLeveltext = f"{row['spellLevel']}nd-level"
        elif row['spellLevel'] == 3:
            spellLeveltext = f"{row['spellLevel']}rd-level"
        else:
            spellLeveltext = f"{row['spellLevel']}th-level"
        retVal = retVal + f"{spellLeveltext} {row['spellSchool']}\n"

        retVal = retVal +  f"**Casting Time:** {row['spellCastingTime']}\n"

        retVal = retVal +  f"**Range:** {row['spellRange']}\n"

        if row["spellMaterials"] is None:
           retVal = retVal + f"**Components:** {row['spellComponents']}\n"
        else:
            retVal = retVal + f"**Components:** {row['spellComponents']} ({row['spellMaterials']})\n"

        if row["spellConcentration"] == "no":
            retVal = retVal + f"**Duration:** {row['spellDuration']}\n"
        else:
            retVal = retVal + f"**Duration:** Concentration, {row['spellDuration']}\n"

        if row['spellArchetype'] is None and not "Ritual Caster" in row['spellClasses']:
            retVal = retVal + f"**Classes**: {row['spellClasses']}\n"
        else:
            spellClasses = row['spellClasses'].split(", ")
            for spellClass in spellClasses:
                if spellClass == "Ritual Caster":
                    ritualCaster = True
                    spellClasses.remove(spellClass)

            retVal = retVal + f"**Classes:** {', '.join(spellClasses)}\n"

            if row['spellArcheType'] is not None:
                retVal = retVal + f"**Available to Subclasses:** {row['spellArchetype']}\n"
            if ritualCaster:
                retVal = retVal + "Spell Available via Ritual Caster Feat\n"

        retVal = retVal + "\n"

        formattedSpellDescription = row['spellDescription'].replace("\\n\\n-\\n\\n","</p><p>").replace("\\n","\n").replace("</p><p>","\n\n").replace("<p>","").replace("</p>","").replace("<b>","**").replace("</b>","**")
        retVal = retVal + f"{formattedSpellDescription}\n\n"
        if row["spellHigherLevel"] is not None:
            formattedSpellHigherLevel = row['spellHigherLevel'].replace("</p><p>","\n\n").replace("<p>","").replace("</p>","").replace("<b>","**").replace("</b>","**")
            retVal = retVal + f"At Higher Levels: {formattedSpellHigherLevel}"
        return retVal



def displaySpellList(spellClass):
    conn = sqlite3.connect('DungeonsNDragons.db')
    conn.row_factory = sqlite3.Row
    table = sqlite3.Cursor
    infoFetched = False
    if spellClass.title() in "Sorcerer|Warlock|Wizard|Cleric|Paladin|Bard|Ranger|Druid":
        infoFetched = True
        table = conn.execute("select * from spells where spellClasses like? or spellArchetype like? order by spellLevel,spellName", (f"%{spellClass}%",f"%{spellClass}%"))
    # retVal = f"__**{spellClass.title()}'s Spell List**__\n\n"
    retVal = ""

    spellList = {
        "spellLevel":[],
        "spellName":[],
        "availableViaSubclass":[],
    }
    # for member in guild.members:
    #     member_list["Name"].append(member.name)
    #     member_list["Status"].append(str(member.status))
    #     if not member.activities:
    #         member_list["Activity"].append('')
    #     else:
    #         member_list["Activity"].append(member.activity.name)
    #     member_list["ID"].append(member.id)

    # df = pd.DataFrame(member_list)
    # return df.to_string(index=False)

    if infoFetched:
        for row in table:
            subclass = ""
            # print(f"{len(spellList['spellLevel'])}|{len(spellList['spellName'])}|{len(spellList['availableViaSubclass'])}")
            if row["spellLevel"] == 0:
                spellList["spellLevel"].append("Cantrip")            
            else:
                spellList["spellLevel"].append(str(row["spellLevel"])) 
            spellList["spellName"].append(row["spellName"])
            if row["spellArchetype"] is not None:
                if spellClass.title() == "Cleric":
                    subclass = row["spellDomains"]
                elif spellClass.title() == "Paladin":
                    subclass = row["spellOaths"]
                elif spellClass.title() == "Druid":
                    subclass = row["spellCircles"]
                elif spellClass.title() == "Warlock":
                    subclass = row["spellPatrons"]
                if subclass is not None:
                    if spellClass.title() in row["spellClasses"].split(', '):
                        spellList["availableViaSubclass"].append(subclass)
                    else:
                        spellList["availableViaSubclass"].append(f"ONLY {subclass}")
                else:
                    spellList["availableViaSubclass"].append("")
            else:
                spellList["availableViaSubclass"].append("")
    if len(spellList["spellName"]) > 0:    
        spellList["spellLevel"].insert(0,"Level")
        spellList["spellName"].insert(0,"Name")
        spellList["availableViaSubclass"].insert(0,"Via SubClass")
        df = pd.DataFrame(spellList)
        retVal = df.to_string(index=False,header=False,justify="start",sparsify=False)
        retValArray = retVal.split("\n")
        retValArray.insert(1,"")
        i = 2
        for string in retValArray[2:]:
            retValArray[i] = string.rstrip()
            i += 1
        retVal = "\n".join(retValArray)
        return retVal




# print(table)