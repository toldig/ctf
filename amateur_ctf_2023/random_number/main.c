#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void generate_canary(int rnd1, int rnd2, int rnd3)
{
    time_t tVar1;
    tVar1 = time((time_t *)0x0);
    int start = tVar1;
    while(tVar1)
    {
        srand((uint)tVar1);
        int canary = rand();
        int tmp_1 = rand();
        int tmp_2 = rand();
        int tmp_3 = rand();
        if ((rnd1 == tmp_1) && (rnd2 == tmp_2) && (rnd3 == tmp_3))
        {
            printf("%d", canary);
            return;
        }
        tVar1--;
    }
    return;
}

void main(int argc, char ** argv)
{
    if (argc != 4)
    {
        printf("Expected 4 arguments!\n");
        return;
    }
    
    generate_canary(atoi(argv[1]), atoi(argv[2]), atoi(argv[3]));
    return;
}
