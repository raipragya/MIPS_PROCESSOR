#include<stdio.h>
int main()
{
  int n;
  printf("Enter a number : ");
  scanf("%d",&n);
  
  int fact=1;
  for (int i=1;i<=n;i++)
  {
    fact=fact*i;
  }
  
  printf("Factorial is : %d\n",fact);
  
  return 0;
  
}
