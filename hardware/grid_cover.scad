//oocyte chamber
//updated by AM Chagas 20210506 -> larger grid
//designed by AM Chagas 20181001 CC BY 4.0 license
//inspired on the design from J Menzies.

wellx = 0.3;
welly = 0.7;
wellz = 5;

interwell = 0.2;

nwellsx = 20;
nwellsy = 20;

platey = wellx*nwellsx*5+5;
platex = welly*nwellsy*1.5+5;
platez = 0.2;






tol = 0.1;
$fn=20;

module grid(){
    for (x = [-nwellsx/2:nwellsx/2]){
        for (y = [-nwellsy/2:nwellsy/2]){
            translate([x*(wellx+interwell),y*(welly+interwell),platez/2-wellz/2+0.01]){
                cube([wellx,welly,wellz],center=true);
                }//end translate
            }//end for y
    }//end for x
}//end module




difference(){

//translate([-platex/2+5,-platey/2+5,-platez+wellz-0.001]){
cube([platex,platey,platez],center=true);

//}

grid();
}





//grid();