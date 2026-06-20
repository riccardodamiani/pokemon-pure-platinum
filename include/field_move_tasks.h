#ifndef POKEPLATINUM_FIELD_MOVE_TASKS_H
#define POKEPLATINUM_FIELD_MOVE_TASKS_H

#include "struct_decls/map_object.h"

#include "field/field_system_decl.h"

#include "field_task.h"
#include "pokemon.h"
#include "generated/items.h"

typedef struct FieldMoveContext {
    u32 mapId;
    FieldSystem *fieldSystem;
    MapObject *mapObj;
    u16 usableMoves;
} FieldMoveContext;

typedef struct FieldMovePokemon {
    FieldTask *fieldTask;
    u16 fieldMonId;
    u16 fieldMove;
} FieldMovePokemon;

enum FieldMoveList {
    FIELD_MOVE_CUT,
    FIELD_MOVE_FLY,
    FIELD_MOVE_SURF,
    FIELD_MOVE_STRENGTH,
    FIELD_MOVE_DEFOG,
    FIELD_MOVE_ROCK_SMASH,
    FIELD_MOVE_WATERFALL,
    FIELD_MOVE_ROCK_CLIMB,
    FIELD_MOVE_FLASH,
    FIELD_MOVE_TELEPORT,
    FIELD_MOVE_DIG,
    FIELD_MOVE_SWEET_SCENT,
    FIELD_MOVE_CHATTER,
    FIELD_MOVE_MILK_DRINK,
    FIELD_MOVE_SOFTBOILED,
    FIELD_MOVE_MAX
};

static const u16 fieldMoveToTMHM[FIELD_MOVE_MAX] = {
    [FIELD_MOVE_CUT] = ITEM_HM01,
    [FIELD_MOVE_FLY] = ITEM_HM02,
    [FIELD_MOVE_SURF] = ITEM_HM03,
    [FIELD_MOVE_STRENGTH] = ITEM_HM04,
    [FIELD_MOVE_DEFOG] = ITEM_HM05,
    [FIELD_MOVE_ROCK_SMASH] = ITEM_HM06,
    [FIELD_MOVE_WATERFALL] = ITEM_HM07,
    [FIELD_MOVE_ROCK_CLIMB] = ITEM_HM08,
    [FIELD_MOVE_FLASH] = ITEM_TM70,
    [FIELD_MOVE_TELEPORT] = ITEM_NONE,
    [FIELD_MOVE_DIG] = ITEM_TM28,
    [FIELD_MOVE_SWEET_SCENT] = ITEM_NONE,
    [FIELD_MOVE_CHATTER] = ITEM_NONE,
    [FIELD_MOVE_MILK_DRINK] = ITEM_NONE,
    [FIELD_MOVE_SOFTBOILED] = ITEM_NONE,
};

static const u16 fieldMoveToMove[FIELD_MOVE_MAX] = {
    [FIELD_MOVE_CUT] = MOVE_CUT,
    [FIELD_MOVE_FLY] = MOVE_FLY,
    [FIELD_MOVE_SURF] = MOVE_SURF,
    [FIELD_MOVE_STRENGTH] = MOVE_STRENGTH,
    [FIELD_MOVE_DEFOG] = MOVE_DEFOG,
    [FIELD_MOVE_ROCK_SMASH] = MOVE_ROCK_SMASH,
    [FIELD_MOVE_WATERFALL] = MOVE_WATERFALL,
    [FIELD_MOVE_ROCK_CLIMB] = MOVE_ROCK_CLIMB,
    [FIELD_MOVE_FLASH] = MOVE_FLASH,
    [FIELD_MOVE_TELEPORT] = MOVE_TELEPORT,
    [FIELD_MOVE_DIG] = MOVE_DIG,
    [FIELD_MOVE_SWEET_SCENT] = MOVE_SWEET_SCENT,
    [FIELD_MOVE_CHATTER] = MOVE_CHATTER,
    [FIELD_MOVE_MILK_DRINK] = MOVE_MILK_DRINK,
    [FIELD_MOVE_SOFTBOILED] = MOVE_SOFTBOILED,
};

enum FieldMoveError {
    FIELD_MOVE_ERROR_NONE,
    FIELD_MOVE_ERROR_LOCATION,
    FIELD_MOVE_ERROR_BADGE,
    FIELD_MOVE_ERROR_PARTNER,
    FIELD_MOVE_ERROR_STATE,
};

enum TaskOrError {
    FIELD_MOVE_TASK,
    FIELD_MOVE_ERROR,
};

typedef struct FlyContext {
    FieldSystem *fieldSystem;
    int state;
    u16 mapID;
    s16 x;
    s16 z;
    Pokemon *mon;
    SysTask *cutInTask;
} FlyContext;

typedef void (*FieldMoveTask)(FieldMovePokemon *, const FieldMoveContext *);
typedef enum FieldMoveError (*FieldMoveErrContext)(const FieldMoveContext *);

FlyContext *FlyContext_New(enum HeapID heapID, FieldSystem *fieldSystem, Pokemon *mon, u16 mapID, s16 x, s16 z);
BOOL FieldMoves_FlyTask(FieldTask *fieldTask);
void *FieldMove_GetTaskOrError(u16 taskOrError, u16 fieldMove);
void FieldMoves_SetUsableMoves(FieldSystem *fieldSystem, FieldMoveContext *fieldMoveContext);

BOOL FieldMoves_CheckMNBadge(const FieldMoveContext *fieldMoveContext, enum FieldMoveList move);
BOOL FieldMoves_CheckHMUsable(const FieldMoveContext *fieldMoveContext, enum FieldMoveList move);

#endif // POKEPLATINUM_FIELD_MOVE_TASKS_H
