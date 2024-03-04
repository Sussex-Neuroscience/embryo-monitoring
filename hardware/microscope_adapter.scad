bpDiam=120;
bpHei = 4;
fibDiam=17;
fibHei=15;

tol=0.1;


cylinder(d=bpDiam-2*tol,h=bpHei);




module fibreCoupler(){
    rotate([0,90,0]){
    difference(){
cylinder(d=fibDiam+4+2*tol,h=fibHei);
translate([0,0,-1]){
cylinder(d=fibDiam+2*tol,h=fibHei+2);
}//end translate
}//end difference
}

}//end module

translate([bpDiam/2-fibHei,0,13]){
fibreCoupler();
}//end translate

translate([-(bpDiam/2),0,13]){
fibreCoupler();
}//end translate