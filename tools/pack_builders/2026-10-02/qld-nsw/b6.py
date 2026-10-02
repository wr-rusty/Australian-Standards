from qb import *
rows = [(1, 900, 12, 24, 60, "C 900 (D 1200 also tabled; no A or B)", "CROSSROADS_WITH_RAILWAY_CROSSINGS_ON_THREE_LEGS", "cross road with railway crossings on the left, right and near legs", "table C: d 480, e 96, f 159, g 225, h 105, k 396"),
        (2, 750, 10, 20, 50, "B 750 (C 900, D 1200 also tabled; no A)", "CROSSROADS_WITH_RAILWAY_CROSSINGS_ON_TWO_LEGS", "cross road with railway crossings on the far and left legs", "table B: d 400, e 80, f 132, g 188, h 88, k 330"),
        (3, 750, 10, 20, 50, "one size, 750, R50, dimensioned directly", "RAILWAY_CROSSING_BETWEEN_T_JUNCTION_AND_CROSSROAD", "railway crossing between a T-junction ahead and a cross road", "sheet dims: 410 / 410 across; down the centre 90 / 80 / 32 / 58 / 50 / 32 / 90 / 45 / 203; 45 / 45 and 215 / 215 at the bottom"),
        (4, 900, 12, 24, 60, "one size, 900, dimensioned directly", "RAILWAY_CROSSING_ON_STAGGERED_SIDE_ROADS", "road with staggered side roads and a railway crossing (tracks each side, crossing gates)", "sheet dims: 354 / 476 across the top, 242 / 285 at the bottom; 445 / 445 and 100 / 125 / 220 / 215 / 105 / 125 down the left"),
        (5, 600, 8, 16, 40, "A 600 (B 750, C 900 also tabled)", "OBLIQUE_RAILWAY_CROSSING_AT_SIDE_ROAD", "road and side road crossed obliquely by a railway", "table A: d 250, e 100, f 250, g 224, h 16, k 120, m 88, n 424"),
        (6, 600, 8, 16, 40, "A 600 (B 750, C 900 also tabled)", "CURVED_RAILWAY_CROSSING_AT_CROSSROAD", "cross road with a curved railway joining a straight one", "table A: d 280, e 220, f 90, g 250"),
        (7, 600, 8, 16, 40, "A 600 (B 750, C 900 also tabled)", "OBLIQUE_RAILWAY_CROSSING_AT_T_JUNCTION", "T-junction with an oblique railway crossing", "table A: d 250, e 150, f 90")]
for n, side, e, b, r, sizes, name, what, dims in rows:
    m = diamond_symbol_spec(f"W7-13-Q01-{n}", f"W7-13-Q01_{n}", f"W7-13-Q01-{n}", side, e, b, r, name + "_YELLOW_DIAMOND", f"({what} symbol)", f"qld_w7-13-q01-{n}_legend", what + ", vector items of the sheet PDF",
        f"Q-series sheet W7-13-Q01_{n} railway level crossing warning sign (2022, page {n} of 7): {what}. Size {sizes}: side {side} drawn as the bounding square {side * R2:.2f}, r {r}, yellow edge {e} + black border {b}. The sheet's vectors are to scale; {dims}.")
    print(n, m)
