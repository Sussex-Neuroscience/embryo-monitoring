    //oocyte chamber
//updated by AM Chagas 20210506 -> larger grid
//designed by AM Chagas 20181001 CC BY 4.0 license
//inspired on the design from J Menzies.

expandValue = 0.2;
wellx = 0.92+expandValue;//0.3
welly = 0.92+expandValue;//0.7
wellz = 0.2;

interwell = 0.4-expandValue;

nwellsx = 10;
nwellsy = 10;

platey = (wellx-0.1)*nwellsx*5+8;//10;
platex = (welly-0.1)*nwellsy*1.5+12;//14;
platez = 2      ;





tol = 0.1;
$fn=20;
/*
module grid(){
    for (x = [0:nwellsx-1]){
        for (y = [0:nwellsy-1]){
            translate([x*(wellx+interwell),y*(welly+interwell),0]){
                cube([wellx,welly,wellz],center=true);
                }//end translate
            }//end for y
    }//end for x
}//end module
*/
module grid(holeThrough=0){
    for (x = [-nwellsx/2+0.5:nwellsx/2-0.5]){
        for (y = [-nwellsy/2+0.5:nwellsy/2-0.5]){
            translate([x*(wellx+interwell),y*(welly+interwell),platez/2-wellz/2+0.01]){
                if(holeThrough==1){
                    cube([wellx,welly,wellz+10],center=true);
                    }//endif
                else{
                 cube([wellx,welly,wellz],center=true);
                    }
                }//end translate
            }//end for y
    }//end for x
}//end module




difference(){


cube([platex,platey,platez],center=true);

grid(holeThrough=1);

for (x=[-platex/2,platex/2]){
    
translate([x,0,0]){
cube([2.1,2.1,10],center=true);
}//end translate
}//end for

for(y=[-platey/2,platey/2]){
translate([0,y,0]){
cube([2.1,2.1,10],center=true);
}//end translate
}//end for
    
}//end difference


/*
translate([-9.5,0,0.05]){
cube([4,15,platez],center=true);
}

translate([9.5,0,0.05]){
cube([4,15,platez],center=true);
}
*/