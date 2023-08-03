

wellx=0.8;
welly=0.4;
wellz=0.41;
tol=0.1;

interwell = 0.8;
nwellsx = 2;
nwellsy = 2;

platey = wellx*nwellsx*5+30;
platex = welly*nwellsy*1.5+14.5;
platez = 2;

screwD = 3;
screwH = 10;

legL=40;
legD=8;


module plate(){
difference(){
translate([0,0,-platez/2+wellz/2-0.01]){
cube([platex,platey,platez],center=true);
}//end translate
translate([0,0,0]){
grid();
}//end translate
}//end difference

}//end module


module grid(){
for (j=[-10:10]){
for(i=[-5:5]){
    translate([i*(wellx/2+interwell),j*(interwell),0]){
        cube([wellx,welly,wellz],center=true);
        }
    }
}
}
plate();