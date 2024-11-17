#include<stdio.h>

int sum_of_squares(int n)
{
  int sum=0;
  while (n!=0)
  {
    int ones=n%10;
    sum=sum+(ones*ones);
    n=n/10;
  }
  
  return sum;
  
}

int main()
{
  int n;
  printf("Enter a number : ");
  scanf("%d",&n);
  printf("Sum of squares of digits is : %d\n",sum_of_squares(n));
  return 0;
}
