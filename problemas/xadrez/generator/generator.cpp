#include <bits/stdc++.h>
using namespace std;

#include "testlib.h"

const char let[6] = {'p','c','t','b','r','k'};
const char qtd[6] = {8,2,2,2,1,1};

char pcs[32];
char mat[8][8];

bool gen_uniform () {
    int n = 0;
    bool ma = 0;

    for (int t = 0; t < 6; t++) {
        for (int ma = 0; ma < 2; ma++) {
            for (int q = 0; q < qtd[t]; q++) {
                pcs[n++] = let[t] + ('A' - 'a')*(ma);
            }
        }
    }

    int pi = -1;
    int pj = -1;
    int q = 0;
    for (int i = 0; i < 8; i++) {
        for (int j = 0; j < 8; j++) {
            if (rnd.next(0,1) && n) {
                int pos = rnd.next(n);
                n--;
                swap(pcs[pos], pcs[n]);
                mat[i][j] = pcs[n];

                if (pcs[n] >= 'A' && pcs[n] <= 'Z' && !rnd.next(0,q++)) {
                    pi = i;
                    pj = j;
                }
            } else {
                mat[i][j] = '.';
            }
        }
    }

    if (pi == -1)
        return 0;

    for (int i = 0; i < 8; i++) {
        for (int j = 0; j < 8; j++)
            putchar(mat[i][j]);
        putchar('\n');
    }
    putchar('a'+pj);
    putchar('8'-pi);
    putchar('\n');
    return 1;
}

int main (int argn, char ** args) {
    registerGen(argn, args, 1);
    while (!gen_uniform());
}
