/*  FuzzySlpPosInference is used to calculate similarity to a kind of slope position
    according to several parameters grid, typical location, and fuzzy inference function.
	Reference:
	[1] �س�־���찢�ˣ�ʩѸ����. ��λ������Ϣ��ģ������[J]. �����о�, 2007, 26(6): 1165-1174.
	[2] Qin C, Zhu A, Shi X, et al. Quantification of spatial gradation of slope positions[J]. Geomorphology, 2009, 110(3): 152-161.
	[3] �س�־��¬�Ҿ��������򣬵�. �����ֵ��η������ (SimDTA) ����Ӧ�á������۽������ɽũ��������λģ������Ϊ��[J]. ������Ϣ��ѧ, 2009, (6): 737-743.
	[4] �س�־���찢�ˣ���֣���. ��λ�ķ��༰��ռ�ֲ���Ϣ�Ķ�����[J]. �人��ѧѧ��: ��Ϣ��ѧ��, 2009, 34(3): 374-377.
	[5] �س�־��¬�Ҿ�����ά����. ģ����λ��Ϣ�ھ�ϸ�������Կռ��Ʋ��е�Ӧ��[J]. �����о�, 2010, 29(9): 1706-1714.
	[6] Qin C, Zhu A, Qiu W, et al. Mapping soil organic matter in small low-relief catchments using fuzzy slope position information[J]. Geoderma, 2012, 171: 64-74.
     
  Liangjun, Zhu
  Lreis, CAS  
  Apr 8, 2015 
  
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <iostream>
#include <fstream>
#include "commonLib.h"
#include "FuzzySlpPosInference.h"
using namespace std;

void split(char *src, const char *separator, char **dest,int *num)
{
	char *pNext;
	int count = 0;
	if(src == NULL || strlen(src) == 0) return;
	if(separator == NULL || strlen(separator) == 0) return;
	pNext = strtok(src,separator);
	while (pNext != NULL)
	{
		*dest++ = pNext;
		++count;
		pNext = strtok(NULL,separator);
	}
	*num = count;
}

int main(int argc, char **argv)
{
	char protogrd[MAXLN],configfile[MAXLN],simfile[MAXLN];
	int prototag = 1; // by default, the tag of prototype GRID is 1, it can also be assigned by user.
	int paramsNum,lineNum = 0,i,err;
	float exponent;
	paramInfGRID *paramsgrd;
	char cfglines[20][MAXLN];
	if(argc == 1)
	{  
		printf("Error: To run this program, use either the Simple Usage option or\n");
		printf("the Usage with Specific file names option\n");
		goto errexit;
	}
	else if (argc == 2)
	{
		strcpy(configfile,argv[1]);
		//printf("%s\n",configfile);
		ifstream cfg(configfile,ios::in);
		while (!cfg.eof())
		{
			cfg.getline(cfglines[lineNum],MAXLN,'\n');
			lineNum++;
		}
		cfg.close();
		char *dest[MAXLN];
		int num,paramline,row = 0;
		while(lineNum > row)
		{
			split(cfglines[row],"\t",dest,&num);
			if(strcmp(dest[0],"PrototypeGRID")==0 && num == 2){
				strcpy(protogrd,dest[1]);
				row++;}
			else if(strcmp(dest[0],"ProtoTag")==0 && num == 2){
				sscanf(dest[1],"%d",&prototag);
				row++;}
			else if(strcmp(dest[0],"ParametersNUM")==0 && num == 2){
				sscanf(dest[1],"%d",&paramsNum);
				paramline = row + 1;
				row = row + paramsNum + 1;}
			else if(strcmp(dest[0],"DistanceExponentForIDW")==0 && num == 2){
				sscanf(dest[1],"%f",&exponent);			
				row++;}
			else if(strcmp(dest[0],"OUTPUT")==0 && num == 2){
				strcpy(simfile,dest[1]);
				row++;}
			else row++;
		}
		paramsgrd = new paramInfGRID[paramsNum];
		i = 0;
		for (row = paramline; row < paramline + paramsNum; row++)
		{
			split(cfglines[row],"\t",dest,&num);
			strcpy(paramsgrd[i].path,dest[1]);
			strcpy(paramsgrd[i].shape,dest[2]);
			sscanf(dest[3],"%f",&paramsgrd[i].w1);
			sscanf(dest[4],"%f",&paramsgrd[i].r1);
			sscanf(dest[5],"%f",&paramsgrd[i].k1);
			sscanf(dest[6],"%f",&paramsgrd[i].w2);
			sscanf(dest[7],"%f",&paramsgrd[i].r2);
			sscanf(dest[8],"%f",&paramsgrd[i].k2);
			if (strcmp(paramsgrd[i].shape,"S")==0)
				if (!(paramsgrd[i].k1 != 1.0 && paramsgrd[i].k2 == 1.0 ))
				{
					printf("Please check the parameters of S-shaped function!\n");
					goto errexit;
				}
			else if (strcmp(paramsgrd[i].shape,"Z")==0)
				if (!(paramsgrd[i].k1 == 1.0 && paramsgrd[i].k2 != 1.0 ))
				{
					printf("Please check the parameters of Z-shaped function!\n");
					goto errexit;
				}
			else
				goto errexit;
			i++;
		}
	}
	else goto errexit;

	if((err=FuzzySlpPosInf(protogrd, prototag,paramsNum, paramsgrd, exponent, simfile))!= 0)
		printf("Error %d\n",err); 
	//system("pause");
	return 0;
errexit:
	printf("Usage with specific config file names:\n %s <configfile>\n",argv[0]);
	printf("The config file should contains context as below:\n");
	printf("PrototypeGRID	path of prototype grid\n");
	printf("ProtoTag	tag of prototype grid\n");
	printf("ParametersNUM	number of parameters grid\n");
	printf("Parameters	path of parameters grid	similarity function type	w1	r1	k1	w2	r2	k2\n");
	printf("DistanceExponentForIDW	float number\n");
	printf("OUTPUT	path of output similarity grid\n");
	exit(0);
}
