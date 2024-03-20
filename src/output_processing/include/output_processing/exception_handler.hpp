#pragma once

#define DLB_ASSERT(cond, msg) \
    if (!(cond))              \
        return false;
