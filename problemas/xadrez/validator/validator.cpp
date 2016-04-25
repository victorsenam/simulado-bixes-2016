#include "testlib.h"

const char let[12] = {'p', 'P', 'c', 'C', 'b', 'B', 't', 'T', 'r', 'R', 'k', 'K'};
const int lim[12] = {8, 8, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1};

int cnt[12];
char mat[8][8];
int main () {
    registerValidation();
    for (int i = 0; i < 8; i++) {
        for (int j = 0; j < 8; j++) {
            char c = inf.readChar();
            mat[i][j] = c;
            bool ok = 0;
            for (int k = 0; !ok && k < 12; k++) {
                if (let[k] == c) {
                    ok = 1;
                    cnt[k]++;

                    if (cnt[k] > lim[k]) {
                        printf("Too many %c\n", let[k]);
                        return 1;
                    }
                }
            }
            if (!ok && c != '.')
                printf("Invalid char %c at (%d,%d)\n", c, i, j);
        }
        inf.readEoln();
    }
    char c = inf.readChar();
    int l = inf.readInt(1, 8);
    c -= 'a';
    l--;
    l = 7 - l;

    if (l < 0 || l >= 8 || c < 0 || c >= 8) {
        printf("Invalid position (%d,%d)\n", l, c);
        return 1;
    }

    bool ok = 0;
    for (int k = 1; k < 12 && !ok; k+=2)
        if (mat[l][c] == let[k])
            ok = 1;
    if (!ok) {
        printf("Given position (%d,%d) is not enemy %c\n", l, c, mat[l][c]);
        return 1;
    }

    inf.readEoln();
    inf.readEof();

    return 0;
}
