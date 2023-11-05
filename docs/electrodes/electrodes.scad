electrode = 4; // radius
handlewidth = 12;
handlethickness = 3;
handlelength = 40;
rodlength = 20; // the narrow bit on which the electrode support rests
rodwidth = 8;
slotwidth = 5;
slotlength = handlelength + rodlength - 20;
standoffwidth=8;
standoffheight=6; // the height of the rectangular bit without the circular head
standoffthickness=2;
standoffdistance=25; // distance from 0,0
wedgelength = 21;
wedgedistance=12; // distance from 0,0
supportwidth=handlewidth-2;

// handle
translate([0, 0, 0])
    handle();  
translate([(handlewidth-slotwidth)/2, wedgedistance, handlethickness])
    wedge();
translate([standoffthickness*2, standoffdistance, handlethickness])
    standoff();
translate([standoffthickness*4, standoffdistance, handlethickness])
    standoff();
translate([supportwidth+((handlewidth-supportwidth)/2), 0, handlethickness])
    support();
translate([handlewidth/2, electrode, handlethickness])
    electrodesupport();

// the flat rectangular part that you squeeze between your fingers
module handle() {
     translate([0, 0, 0]) {
        difference() {
            union() {
                translate([(handlewidth-rodwidth)/2, 0, 0])
                    color("red") cube([rodwidth, rodlength, handlethickness]);
                translate([0, rodlength, 0])
                    cube([handlewidth, handlelength, handlethickness]);
            }
            // slot inside the handle
            translate([(handlewidth/2)-(slotwidth/2) , handlelength + rodlength - slotlength - 10, 0]) {
                cube([slotwidth, slotlength, handlethickness]);
            }
        }
    }
}

// the triagular bit into which the standoffs fit
module support() {
    radius = 4;
    rotate([0, -90, 0]) {
        difference() {
            difference()  {
                linear_extrude(supportwidth) {
                    polygon([[0, 20], [0, 50], [3, 40], [3, 20]]);
                }
                translate([0, 0, (supportwidth - slotwidth) / 2])
                    color("red") linear_extrude(slotwidth) {
                        polygon([[0, 50], [3, 40], [3, 25], [0, 25]]);
                    }
            }
            translate([4.5, 29, 0]) {
                cylinder(handlewidth, radius+.5, radius+.5, $fn=100);
            }
        }
    }
}


// the bit where the electrode fits on
module electrodesupport() {
    cylinder(3, electrode, electrode, $fn=100);
}

// the bits in the middle that fit the two parts togehter
module standoff() {
    rotate([0, -90, 0]) {
        color("blue") cube([standoffheight, standoffwidth, standoffthickness]);
        translate([standoffheight, standoffwidth/2, 0]) {
            cylinder(standoffthickness, standoffwidth/2, standoffwidth/2, $fn=100);
        }
    }
}

// the wedge in the slot which keeps the spring in place
module wedge() {
    rotate([0, 90, 0])
    color("green") linear_extrude(slotwidth) {
        polygon([[0,0], [0, wedgelength], [1, wedgelength], [2, 0]]);
    }
}