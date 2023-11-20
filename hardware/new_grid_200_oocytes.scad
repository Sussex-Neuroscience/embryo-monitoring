//oocyte chamber
//updated by AM Chagas 20210506 -> larger grid
//designed by AM Chagas 20181001 CC BY 4.0 license
//inspired on the design from J Menzies.

wellx = 0.3;
welly = 0.7;
wellz = 0.2;

interwell = 0.4;

nwellsx = 20;
nwellsy = 10;

platey = wellx*nwellsx*5+10;
platex = welly*nwellsy*1.5+14;
platez = 0.5;








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
    for (x = [-nwellsx/2:nwellsx/2]){
        for (y = [-nwellsy/2:nwellsy/2]){
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

//translate([-platex/2+5,-platey/2+5,-platez+wellz-0.001]){
cube([platex,platey,platez],center=true);

//}

grid(holeThrough=1);
}
translate([-9.5,0,0.05]){
cube([4,15,platez],center=true);
}

translate([9.5,0,0.05]){
cube([4,15,platez],center=true);
}