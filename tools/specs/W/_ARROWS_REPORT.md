# W family - geometric arrow conversions

Format: `CODE symbol-id - STATUS (detail)`. Overlays of the previous traced output against the new geometric output were checked for every line marked CONVERTED (both hands where handed); differences are trace-noise fringes only.

W1-1 w1-1_turn_arrow_l - CONVERTED
W1-3 w1-3_curve_arrow_l - CONVERTED
W1-2 w1-2_reverse_turn_arrow_l - CONVERTED (inset is the R hand; turns flipped for drawn_hand L; R25/R15 taken for both corners, the inset labels each once on a point-symmetric shape)
W1-4 w1-4_reverse_curve_arrow_l - CONVERTED (S-bend sweep 54.70 deg / straight 179.30 solved from the stated 235 jog, R50 inner/R160 outer and 95/25/520 heights; inset is the R hand, flipped)
W1-7 w1-7_hairpin_arrow_l - CONVERTED (head 170 long = 205 - 35; 180 deg arc written as two 90 deg arcs so the arc top enters the box check; inset is the R hand, flipped)
W1-8-2 w1-8_curve_arrow_l - CONVERTED
W1-8-3 w1-8_turn_arrow_l - CONVERTED (sheet's 1140 read as the overall height, arm centreline 850, as the curve arrow's 270 + 580 + 290 = 1140 confirms)
W1-8-4 w1-8_reverse_curve_arrow_l - CONVERTED (S-bend sweep 54.70 deg / straight 358.61 solved from 470 jog, R100/R320, 190/50/1040; sheet is the R hand, flipped)
W1-8-5 w1-8_hairpin_arrow_l - ISSUE (converted from the sheet: 825 + R390 = 1215 tall, head 340 = 410 - 70; the spec box is 1270 tall (QA chain closure) and the W1-8-5 drawing states 1230, so the generator flags arrow-size 1215 vs 1270; arrow is centred in the box as the traced one was - the drawing's vertical chain 130+1336+69+45+1230+150 = 2960 does not close and needs a decision)
W1-9-2 w1-9-2_curve_arrow_l - CONVERTED (sweep not stated; 75 deg derived from the stated 653 x 655 extents, gives 657.5 x 654.2)
W1-9-3 w1-9-3_turn_arrow_l - CONVERTED
W1-9-4 w1-9-4_reverse_curve_arrow_r - CONVERTED (drawn R hand; S-bend sweep 54.54 deg / straight 191.96 from 250 jog, R170 outer, 101/394; 5 straight under the head = 655 - 256 - 394, the inset's 394 + 256 = 650 vs 655 is a 5 mm inconsistency in the drawing)
W1-9-5 w1-9-5_hairpin_arrow_l - KEPT TRACED (missing: head notch depth not stated; inset's 429 + R210 = 639 does not match the stated 655 height)
W3-1 w3-1_up_arrow - CONVERTED (81 shaft, head 125 x 250, notch 16, R8)
W3-2 w3-1_up_arrow - CONVERTED (W3-2 drawing gives only the 219 height; W3-1 inset dims used as the spec already did)
W3-4-1 w3-1_up_arrow - CONVERTED (inset repeats the W3-1 dims)
W3-4-2 w3-1_up_arrow - CONVERTED (per-hand arrows heading -135/-45; boxes computed so the rotation centre is unchanged)
W3-4-3 w3-1_up_arrow - CONVERTED (per-hand arrows heading 180/0)
WM3-2A w3-1_up_arrow - KEPT TRACED (missing: the WM3-2A drawing gives only the 133 arrow height; no width or head dims)
W4-10 w4-10_arrow_up - CONVERTED (tapered shaft 50 -> 66, not expressible by the arrow engine; drawn as polygons with R10 barbs from the inset)
W4-11 w4-11_arrow_up - CONVERTED (tapered shaft 62 -> 82; polygons with R12 barbs)
W8-3 w8-3_arrow - CONVERTED (tapered shaft 29 -> 39; polygon with R5 barbs, mirrors for R)
W8-15 w8-3_arrow - CONVERTED (same polygon pointing right)
W8-23 w8-23_double_arrow - CONVERTED (two arrow elements sharing the 44 shaft, 112 + 138 each side)
W5-34 w5-34_merge_arrow - KEPT TRACED (composite merge picture: arrow plus a 45 deg branch joined by an R252 arc)
W5-35 w5-35_lane_merge - KEPT TRACED (composite: two arrows, island and curved lane; not a plain arrow)
W4-1 w4-1_narrow_bridge - KEPT TRACED (kinked bars, not straight bars; not an arrow)
W4-3 w4-3_road_narrows - KEPT TRACED (bent bars; bend offsets not fully stated)
W4-4 w4-4_divided_road - KEPT TRACED (Y-shaped composite with R75/R178/R119 arcs)
