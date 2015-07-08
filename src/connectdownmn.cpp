/*  Connect Down main program 
     
  David Tarboton
  Utah State University  
  July 11, 2012 
  

  This function reads an ad8 contributing area file, 
  identifies the location of the largest ad8 value as the outlet of the largest watershed and writes a shapefile at these locations.
  It then reads the flow direction grid and moves the points down direction a designated number of grid cells and writes a shapefile

*/

/*  Copyright (C) 2010  David Tarboton, Utah State University

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License 
version 2, 1991 as published by the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

A copy of the full GNU General Public License is included in file 
gpl.html. This is also available at:
http://www.gnu.org/copyleft/gpl.html
or from:
The Free Software Foundation, Inc., 59 Temple Place - Suite 330, 
Boston, MA  02111-1307, USA.

If you wish to use or incorporate this program (or parts of it) into 
other software that does not meet the GNU General Public License 
conditions contact the author to request permission.
David G. Tarboton  
Utah State University 
8200 Old Main Hill 
Logan, UT 84322-8200 
USA 
http://www.engineering.usu.edu/dtarb/ 
email:  dtarb@usu.edu 
*/

//  This software is distributed from http://hydrology.usu.edu/taudem/
  
#include <time.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include "commonLib.h"
#include "connectdown.h"

int main(int argc,char **argv)
{
   char ad8file[MAXLN],outletshapefile[MAXLN];
   int err,i,movedist=10;
   if(argc < 5)
    {  
       printf("No simple use case for this function.\n");
	   goto errexit;
    }
	i = 1;
	while(argc > i)
	{
		if(strcmp(argv[i],"-ad8")==0)
		{
			i++;
			if(argc > i)
			{
				strcpy(ad8file,argv[i]);
				i++;
			}
			else goto errexit;
		}
		else if(strcmp(argv[i],"-o")==0)
		{
			i++;
			if(argc > i)
			{
				strcpy(outletshapefile,argv[i]);
				i++;
			}
			else goto errexit;
		}
		else 
		{
			goto errexit;
		}
	}
	err=connectdown(ad8file, outletshapefile);
    if(err != 0)
       printf("Creating outlet error %d\n",err);

	return 0;
errexit:
	   printf("Incorrect input.\n");
	   printf("Use with specific file names:\n %s -ad8 <ad8file> -o <outletsshapefile>\n ",argv[0]);
	   printf("<ad8file> is the name of the contributing raster file (input).\n");
	   printf("<outletsshapefile> is the name of the outlet shape file (input).\n");
       exit(0);
} 

