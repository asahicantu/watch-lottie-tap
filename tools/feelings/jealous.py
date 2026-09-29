from feeling_parts import backdrop, brows, eyes, gloom_lines, head, pout, sway

COLOR = "#7CB342"


def jealous():
    return [
        gloom_lines(color="#3E7A1E", opacity=60),
        pout((4, 50), rotation=6),
        *brows(y=-27, tilt=-12, arch=2),
        # green-eyed side-eye under heavy lids
        *eyes(w=30, h=24, lid=0.45, look=(8, 1), iris="#5E8C31"),
        head(cheeks=25),
        backdrop(COLOR),
    ], lambda layer: sway(layer, amp=5, period=45)
