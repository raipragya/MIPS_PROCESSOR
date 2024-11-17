#include <stdio.h>

int compare(int arr[],int n)
{
	int max=arr[0];
	for (int i=1;i<n;i++)
	{
		if (arr[i]>max)
			max=arr[i];
	}
	return max;
}

void main()
{
	int a[10];		//declare array
	int n;
	printf("Enter the number of elements:");
	scanf("%d",&n);
	for (int i=0;i<n;i++)
	{
		scanf("%d",&a[i]);
	}
	printf("The maximum element is %d.\n",compare(a,n));
}
