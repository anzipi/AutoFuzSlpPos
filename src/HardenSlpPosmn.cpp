/*  HardenSlpPos is used to generate hard class of slope positions.
	Reference:
	[1] �س�־���찢�ˣ�ʩѸ����. ��λ������Ϣ��ģ������[J]. �����о�, 2007, 26(6): 1165-1174.
	[2] Qin C, Zhu A, Shi X, et al. Quantification of spatial gradation of slope positions[J]. Geomorphology, 2009, 110(3): 152-161.
	[3] �س�־��¬�Ҿ��������򣬵�. �����ֵ��η������ (SimDTA) ����Ӧ�á������۽������ɽũ��������λģ������Ϊ��[J]. ������Ϣ��ѧ, 2009, (6): 737-743.
	[4] �س�־���찢�ˣ���֣���. ��λ�ķ��༰��ռ�ֲ���Ϣ�Ķ�����[J]. �人��ѧѧ��: ��Ϣ��ѧ��, 2009, 34(3): 374-377.
	[5] �س�־��¬�Ҿ�����ά����. ģ����λ��Ϣ�ھ�ϸ�������Կռ��Ʋ��е�Ӧ��[J]. �����о�, 2010, 29(9): 1706-1714.
	[6] Qin C, Zhu A, Qiu W, et al. Mapping soil organic matter in small low-relief catchments using fuzzy slope position information[J]. Geoderma, 2012, 171: 64-74.
     
  Liangjun, Zhu
  Lreis, CAS  
  Apr 13, 2015 
  
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <iostream>
#include <fstream>
#include "commonLib.h"
#include "HardenSlpPos.h"
using namespace std;

int main(int argc, char **argv)
{
	char rdgfile[MAXLN],shdfile[MAXLN],bksfile[MAXLN],ftsfile[MAXLN],vlyfile[MAXLN]; // input
	char hardfile[MAXLN],maxsimifile[MAXLN],sechardfile[MAXLN],secsimifile[MAXLN]; // output
	bool calSPSI = false;
	bool calSec = false;
	int SPSImodel = 1;
	char spsifile[MAXLN];
	int i,err;
	if(argc == 1)
	{  
		printf("Error: To run this program, use either the Simple Usage option or\n");
		printf("the Usage with Specific file names option\n");
		goto errexit;
	}
	else if (argc > 12)  // at least, there should be 13 input parameters
	{
		i = 1;	
		while(argc > i)
		{
			if(strcmp(argv[i],"-rdg")==0)
			{
				i++;
				if(argc > i)
				{
					strcpy(rdgfile,argv[i]);
					i++;
				}
				else goto errexit;
			}
			else if(strcmp(argv[i],"-shd")==0)
			{
				i++;
				if(argc > i)
				{
					strcpy(shdfile,argv[i]);
					i++;
				}
				else goto errexit;
			}
			else if(strcmp(argv[i],"-bks")==0)
			{
				i++;
				if(argc > i)
				{
					strcpy(bksfile,argv[i]);
					i++;
				}
				else goto errexit;
			}
			else if(strcmp(argv[i],"-fts")==0)
			{
				i++;
				if(argc > i)
				{
					strcpy(ftsfile,argv[i]);
					i++;
				}
				else goto errexit;
			}
			else if(strcmp(argv[i],"-vly")==0)
			{
				i++;
				if(argc > i)
				{
					strcpy(vlyfile,argv[i]);
					i++;
				}
				else goto errexit;
			}
			else if(strcmp(argv[i],"-maxS")==0)
			{
				i++;
				if(argc > i)
				{
					strcpy(hardfile,argv[i]);
					i++;
				}
				if (argc > i)
				{
					strcpy(maxsimifile,argv[i]);
					i++;
				}
				else goto errexit;
			}
			else if(strcmp(argv[i],"-secS")==0)
			{
				i++;
				if(argc > i)
				{
					strcpy(sechardfile,argv[i]);
					i++;
				}
				if (argc > i)
				{
					strcpy(secsimifile,argv[i]);
					calSec = true;
					i++;
				}
				else goto errexit;
			}
			else if(strcmp(argv[i],"-m")==0)
			{
				i++;
				if(argc > i)
				{
					sscanf(argv[i],"%d",&SPSImodel);
					i++;
				}
				if (argc > i)
				{
					strcpy(spsifile,argv[i]);
					calSPSI = true;
					i++;
				}
				else goto errexit;
			}
			else goto errexit;
		}
	}
	else 
	{
		printf("No simple use option for this function because slope position similarity files are needed.\n", argv[0]);
		goto errexit;
	}

	// test if the input is correct!
	//printf("RDG:%s\n",rdgfile);
	//printf("SHD:%s\n",shdfile);
	//printf("BKS:%s\n",bksfile);
	//printf("FTS:%s\n",ftsfile);
	//printf("VLY:%s\n",vlyfile);
	//printf("Hard:%s\n",hardfile);
	//printf("MaxSimi:%s\n",maxsimifile);
	//if (calSec)
	//{
	//	printf("SecHard:%s\n",sechardfile);
	//	printf("SecMaxSimi:%s\n",secsimifile);
	//}
	//if (calSPSI)
	//{
	//	printf("SPSI:%s\n",spsifile);
	//}
	// end test
	if((err=HardenSlpPos(rdgfile,shdfile,bksfile,ftsfile,vlyfile,hardfile,maxsimifile,calSec,sechardfile,secsimifile,calSPSI,SPSImodel,spsifile))!= 0)
		printf("Error %d\n",err); 
	//system("pause");
	return 0;
errexit:
	printf("Usage with specific config file names:\n %s <configfile>\n",argv[0]);
	printf("-rdg <rdgfile> -shd <shdfile> -bks <bksfile> -fts <ftsfile> -vly <vlyfile>\n");
	printf("-maxS <hardfile> <maxsimifile> [-secS <sechardfile> <secsimifile>]\n");
	printf("[-m SPSImodel <SPSIfile>]\n");
	printf("<rdgfile> is the similarity to ridge\n");
	printf("<shdfile> is the similarity to shoulder slope\n");
	printf("<bksfile> is the similarity to back slope\n");
	printf("<ftsfile> is the similarity to foot slope\n");
	printf("<vlyfile> is the similarity to valley\n");
	printf("<hardfile> is the hard slope position\n");
	printf("<maxsimifile> is the maximum similarity\n");
	printf("<sechardfile> is the second hard slope position\n");
	printf("<secsimifile> is the second maximum similarity\n");
	printf("SPSImodel can be 1, 2 and 3, which means \n");
	printf("    Model 1: [HardCls] + sgn([2ndHardCls]-[HardCls]) * (1-[MaxSim])/2\n");
	printf("    Model 2: [HardCls] + sgn([2ndHardCls]-[HardCls]) * (1-([MaxSim]-[2ndMaxSim]))/2\n");
	printf("    Model 3: [HardCls] + sgn([2ndHardCls]-[HardCls]) * ([2ndMaxSim]/[MaxSim])/2\n");
	printf("<sechardfile> is the second hard slope position\n");
	exit(0);
}