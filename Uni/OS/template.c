#include <stdio.h>
#include "transact.h"
#include <pthread.h>

// 100000000

void *process(void *arg)
{
}

int count = 100;

int main(int argc, char *argv[])
{

  int threadNum = atoi(argv[1]);
  int funcNum = atoi(argv[2]);
  int transaction = 0;

  for (int i = 0; i < count / threadNum; i++)
  {
    if (funcNum == 0)
    {
      int transaction = getTransaction(i);
    }
    if (funcNum == 1)
    {
      int transaction = getTransactionFromFile(i);
    }

    printf("%d : %d\n", i, transaction);
  }
}
