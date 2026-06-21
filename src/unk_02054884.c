#include "unk_02054884.h"

#include <nitro.h>
#include <string.h>

#include "constants/battle/condition.h"
#include "constants/field_poison.h"
#include "constants/heap.h"
#include "constants/items.h"

#include "overlay005/daycare.h"

#include "heap.h"
#include "party.h"
#include "pokemon.h"
#include "save_catchrecords.h"
#include "save_player.h"
#include "savedata.h"
#include "trainer_info.h"
#include "unk_02017038.h"
#include "bag.h"

BOOL Pokemon_CanBattle(Pokemon *mon)
{
    // this can be simplified further, but it won't match
    if (Pokemon_GetValue(mon, MON_DATA_HP, NULL) == 0) {
        return FALSE;
    }

    return !Pokemon_GetValue(mon, MON_DATA_IS_EGG, NULL);
}

BOOL Pokemon_GiveMonFromScript(enum HeapID heapID, SaveData *saveData, u16 species, u8 level, u16 heldItem, int metLocation, int metTerrain)
{
    BOOL result;
    Pokemon *mon;
    u32 item;
    Party *party;
    TrainerInfo *trainerInfo = SaveData_GetTrainerInfo(saveData);

    party = SaveData_GetParty(saveData);
    mon = Pokemon_New(heapID);

    Pokemon_Init(mon);
    Pokemon_InitWith(mon, species, level, INIT_IVS_RANDOM, 0, 0, FALSE, 0, OTID_NOT_SET, 0);
    Pokemon_SetCatchData(mon, trainerInfo, ITEM_POKE_BALL, metLocation, metTerrain, heapID);

    item = heldItem;
    Pokemon_SetValue(mon, MON_DATA_HELD_ITEM, &item);
    result = Party_AddPokemon(party, mon);

    if (result) {
        SaveData_UpdateCatchRecords(saveData, mon);
    }

    Heap_Free(mon);

    return result;
}

BOOL sub_02054930(int unused, SaveData *saveData, u16 param2, u8 param3, int param4, int param5)
{
    int v0;
    BOOL result;
    TrainerInfo *trainerInfo = SaveData_GetTrainerInfo(saveData);
    Party *party = SaveData_GetParty(saveData);
    Pokemon *mon = Pokemon_New(HEAP_ID_FIELD3);

    Pokemon_Init(mon);

    v0 = SpecialMetLoc_GetId(param4, param5);
    Egg_CreateEgg(mon, param2, param3, trainerInfo, 4, v0);

    result = Party_AddPokemon(party, mon);
    Heap_Free(mon);

    return result;
}

void Party_ResetMonMoveSlot(Party *party, int partySlot, int moveSlot, u16 moveID)
{
    Pokemon_ResetMoveSlot(Party_GetPokemonBySlotIndex(party, partySlot), moveID, moveSlot);
}

u16 MoveToTM(u16 move){
    switch (move) {
    case MOVE_CUT:
        return ITEM_HM01;
    case MOVE_FLY:
        return ITEM_HM02;
    case MOVE_SURF:
        return ITEM_HM03;
    case MOVE_STRENGTH:
        return ITEM_HM04;
    case MOVE_DEFOG:
        return ITEM_HM05;
    case MOVE_ROCK_SMASH:
        return ITEM_HM06;
    case MOVE_WATERFALL:
        return ITEM_HM07;
    case MOVE_ROCK_CLIMB:
        return ITEM_HM08;
    case MOVE_FLASH:
        return ITEM_TM70;
    case MOVE_TELEPORT:
        return ITEM_NONE;
    case MOVE_DIG:
        return ITEM_TM28;
    case MOVE_SWEET_SCENT:
        return ITEM_NONE;
    case MOVE_CHATTER:
        return ITEM_NONE;
    case MOVE_MILK_DRINK:
        return ITEM_NONE;
    case MOVE_SOFTBOILED:
        return ITEM_NONE;
    default:
        return ITEM_NONE;
    }
}

BOOL Party_CanMonUseFieldMove(Party *party, Bag* bag, u16 move, u8* outMonSlot){
    u16 TMItem = MoveToTM(move);
    u8 TMId = TMItem - ITEM_TM01;

    u8 partyCount = Party_GetCurrentCount(party);
    if(outMonSlot != NULL) {
        *outMonSlot = MAX_PARTY_SIZE;
    }

    BOOL TM_InBag = FALSE;

    // search for the TM/HM in bag
    if(TMItem != ITEM_NONE){
        u32 i;
        for (i = 0; i < TMHM_POCKET_SIZE; i++) {
            if (bag->tmHms[i].item == TMItem) {
                if(bag->tmHms[i].quantity > 0){
                    TM_InBag = TRUE;
                }
                break;
            }
        }
    }


    for(int monSlot = 0; monSlot < partyCount; monSlot++){
        BOOL pokemonHasMove = FALSE;
        Pokemon *mon = Party_GetPokemonBySlotIndex(party, monSlot);

        if (Pokemon_GetValue(mon, MON_DATA_IS_EGG, NULL)) {
            continue;
        }
        
        if(TMItem != ITEM_NONE){
            // finds out if the pokemon knows the move
            int monMoveId;
            for (monMoveId = 0; monMoveId < 4; monMoveId++) {
                u16 monMove = (u16)Pokemon_GetValue(mon, MON_DATA_MOVE1 + monMoveId, NULL);

                if (monMove == 0) {
                    break;
                }

                if(monMove == move){
                    pokemonHasMove = TRUE;
                    break;
                }
            }
        }

        // TM/HM moves
        if(TMItem != ITEM_NONE &&
            (TM_InBag || pokemonHasMove) && // the TM/HM is in the bag or already learned by the mon
            Pokemon_CanLearnTM(mon, TMId)){     // the pokemon can learn it

            if(outMonSlot != NULL) {
                *outMonSlot = monSlot;
            }
            return TRUE;
        }

        // Level up moves
        if(Pokemon_LearnByLevelUp(mon, move)){
            if(outMonSlot != NULL) {
                *outMonSlot = monSlot;
            }
            return TRUE;
        }
    }

    return FALSE;
}

// In many of the functions below, C99-style iterator declaration doesn't match

int Party_HasMonWithMove(Party *party, u16 moveID)
{
    int i;
    int partyCount = Party_GetCurrentCount(party);

    for (i = 0; i < partyCount; i++) {
        Pokemon *mon = Party_GetPokemonBySlotIndex(party, i);

        if (Pokemon_GetValue(mon, MON_DATA_IS_EGG, NULL) != FALSE) {
            continue;
        }

        if (Pokemon_GetValue(mon, MON_DATA_MOVE1, NULL) == moveID
            || Pokemon_GetValue(mon, MON_DATA_MOVE2, NULL) == moveID
            || Pokemon_GetValue(mon, MON_DATA_MOVE3, NULL) == moveID
            || Pokemon_GetValue(mon, MON_DATA_MOVE4, NULL) == moveID) {
            return i;
        }
    }

    return PARTY_SLOT_NONE;
}

int Party_AliveMonsCount(const Party *party)
{
    int i;
    int partyCount = Party_GetCurrentCount(party);
    int count = 0;

    for (i = 0; i < partyCount; i++) {
        if (Pokemon_CanBattle(Party_GetPokemonBySlotIndex(party, i))) {
            count++;
        }
    }

    return count;
}

Pokemon *Party_FindFirstEligibleBattler(const Party *party)
{
    int i;
    int partyCount = Party_GetCurrentCount(party);

    for (i = 0; i < partyCount; i++) {
        Pokemon *mon = Party_GetPokemonBySlotIndex(party, i);

        if (Pokemon_CanBattle(mon)) {
            return mon;
        }
    }

    GF_ASSERT(FALSE);
    return NULL;
}

Pokemon *Party_FindFirstHatchedMon(const Party *party)
{
    u16 i;
    u16 partyCount = Party_GetCurrentCount(party);

    for (i = 0; i < partyCount; i++) {
        Pokemon *mon = Party_GetPokemonBySlotIndex(party, i);

        if (Pokemon_GetValue(mon, MON_DATA_IS_EGG, NULL) == FALSE) {
            return mon;
        }
    }

    return NULL;
}

BOOL Party_HasTwoAliveMons(const Party *party)
{
    return Party_AliveMonsCount(party) >= 2;
}

void Party_GiveChampionRibbons(Party *party)
{
    int i;
    u8 championRibbon = TRUE;
    int partyCount = Party_GetCurrentCount(party);

    for (i = 0; i < partyCount; i++) {
        Pokemon *mon = Party_GetPokemonBySlotIndex(party, i);

        if (Pokemon_GetValue(mon, MON_DATA_IS_EGG, NULL) == FALSE) {
            Pokemon_SetValue(mon, MON_DATA_SINNOH_CHAMP_RIBBON, &championRibbon);
        }
    }
}

int Pokemon_DoPoisonDamage(Party *party, u16 mapLabelTextID)
{
    int numPoisoned = 0;
    int numFainted = 0;
    int i, partyCount = Party_GetCurrentCount(party);
    Pokemon *mon;

    for (i = 0; i < partyCount; i++) {
        mon = Party_GetPokemonBySlotIndex(party, i);

        if (Pokemon_CanBattle(mon)
            && (Pokemon_GetValue(mon, MON_DATA_STATUS, NULL) & (MON_CONDITION_TOXIC | MON_CONDITION_POISON))) {
            u32 hp = Pokemon_GetValue(mon, MON_DATA_HP, NULL);

            if (hp > 1) {
                hp--;
            }

            Pokemon_SetValue(mon, MON_DATA_HP, &hp);

            if (hp == 1) {
                numFainted++;
                Pokemon_UpdateFriendship(mon, FRIENDSHIP_EVENT_POISON_SURVIVE, mapLabelTextID);
            }

            numPoisoned++;
        }
    }

    if (numFainted) {
        return FLDPSN_FAINTED;
    } else if (numPoisoned) {
        return FLDPSN_POISONED;
    } else {
        return FLDPSN_NONE;
    }
}

BOOL Pokemon_TrySurvivePoison(Pokemon *mon)
{
    if (Pokemon_GetValue(mon, MON_DATA_STATUS, NULL) & (MON_CONDITION_TOXIC | MON_CONDITION_POISON)
        && Pokemon_GetValue(mon, MON_DATA_HP, NULL) == 1) {
        u32 condition = MON_CONDITION_NONE;

        Pokemon_SetValue(mon, MON_DATA_STATUS, &condition);
        return TRUE;
    }

    return FALSE;
}
