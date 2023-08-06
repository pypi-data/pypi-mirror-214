from utnamtte import tte
import math


def gcd(n, d):
    if d == 0:
        return n
    else:
        return gcd(d, n % d)


def circum_xnum(x1, x2, x3, y1, y2, y3):
    xnum = eval(
        tte(f"({x1}^2 + {y1}^2)({y2} - {y3}) + ({x2} ^ 2 + {y2} ^ 2)({y3} - {y1}) + ({x3} ^ 2 + {y3} ^ 2)({y1} - {y2})"))
    return xnum


def circum_xden(x1, x2, x3, y1, y2, y3):
    xden = 2 * eval(tte(f"{x1}({y2}-{y3})+{x2}({y3}-{y1})+{x3}({y1}-{y2})"))
    return xden


def circum_ynum(x1, x2, x3, y1, y2, y3):
    ynum = eval(
        tte(f"({x1}^2 + {y1}^2)({x2} - {x3}) + ({x2} ^ 2 + {y2} ^ 2)({x3} - {x1}) + ({x3} ^ 2 + {y3} ^ 2)({x1} - {x2})"))
    return ynum


def circum_yden(x1, x2, x3, y1, y2, y3):
    yden = 2 * eval(tte(f"{y1}({x2}-{x3})+{y2}({x3}-{x1})+{y3}({x1}-{x2})"))
    return yden


def iscollinear_3d(x1, y1, z1, x2, y2, z2, x3, y3, z3):
    x1 = eval(tte(x1))
    x2 = eval(tte(x2))
    x3 = eval(tte(x3))

    y1 = eval(tte(y1))
    y2 = eval(tte(y2))
    y3 = eval(tte(y3))

    z1 = eval(tte(z1))
    z2 = eval(tte(z2))
    z3 = eval(tte(z3))

    if (x1-x2)*(y2-y3) == (x2-x3)*(y1-y2) and (y1-y2)*(z2-z3) == (y2-y3)*(z1-z2) and (x1-x2)*(z2-z3) == (x2-x3)*(z1-z2):
        return True

    else:
        return False


def iscollinear(x1, x2, x3, y1, y2, y3):
    x1 = eval(tte(x1))
    x2 = eval(tte(x2))
    x3 = eval(tte(x3))
    y1 = eval(tte(y1))
    y2 = eval(tte(y2))
    y3 = eval(tte(y3))
    if (y1 - y2) * (x2 - x3) == (x1 - x2) * (y2 - y3) or (y2 - y3) * (x3 - x1) == (x2 - x3) * (y3 - y1) or (y1 - y2) * (
            x3 - x1) == (x1 - x2) * (y3 - y1):
        return True
    else:
        return False


def intersect(x1, y1, z1, x2, y2, z2, a1n, a1d, b1n, b1d, c1n, c1d, a2n, a2d, b2n, b2d, c2n, c2d):
    # print("---------intersect-----------")
    x1 = eval(tte(x1))
    x2 = eval(tte(x2))
    y1 = eval(tte(y1))
    y2 = eval(tte(y2))
    z1 = eval(tte(z1))
    z2 = eval(tte(z2))
    a1n = eval(tte(a1n))
    a1d = eval(tte(a1d))
    a2n = eval(tte(a2n))
    a2d = eval(tte(a2d))
    b1n = eval(tte(b1n))
    b1d = eval(tte(b1d))
    b2n = eval(tte(b2n))
    b2d = eval(tte(b2d))
    c1n = eval(tte(c1n))
    c1d = eval(tte(c1d))
    c2n = eval(tte(c2n))
    c2d = eval(tte(c2d))
    ln = 0
    ld = 0
    if a1n * a2d == a2n * a1d and b1n * b2d == b2n * b1d and c1n * c2d == c2n * c1d:
        return "same line", "same line", "same line", "no data", "no data", "no data"
    else:

        if (a1n * b2n * a2d * b1d - a2n * b1n * a1d * b2d) != 0:
            ln = (a2n * b2d * (y1 - y2) - b2n * a2d * (x1 - x2)) * a1d * b1d
            ld = (a1n * b2n * a2d * b1d - a2n * b1n * a1d * b2d)
        # print("1st l", ln/ld)

        else:
            if (a1n * c2n * a2d * c1d - a2n * c1n * a1d * c2d) != 0:
                ln = (a2n * c2d * (z1 - z2) - c2n * a2d * (x1 - x2)) * a1d * c1d
                ld = (a1n * c2n * a2d * c1d - a2n * c1n * a1d * c2d)
            # print("2nd l", ln/ld)

            else:
                if (b1n * c2n * b2d * c1d - b2n * c1n * b1d * c2d) != 0:
                    ln = (b2n * c2d * (z1 - z2) - c2n * b2d * (x1 - x2)) * b1d * c1d
                    ld = (b1n * c2n * b2d * c1d - b2n * c1n * b1d * c2d)
                    # print("3rd l", ln/ld)
        # print("l once again", ln,"/",ld)
        # print("x3", x1)
        # print("y3", y1)
        # print("z3", z1)
        # print("x4", x2)
        # print("y4", y2)
        # print("z4", z2)
        xf = (a1n * ln + x1 * ld * a1d) / (ld * a1d)
        x_num = (a1n * ln + x1 * ld * a1d)
        x_den = (ld * a1d)
        x_gcd = gcd(x_num, x_den)
        x_num = x_num / x_gcd
        x_den = x_den / x_gcd
        x_fraction = f"{x_num} / {x_den}"
        yf = (b1n * ln + y1 * ld * b1d) / (ld * b1d)
        y_num = (b1n * ln + y1 * ld * b1d)
        y_den = (ld * b1d)
        y_gcd = gcd(y_num, y_den)
        y_num = y_num / y_gcd
        y_den = y_den / y_gcd
        y_fraction = f"{y_num} / {y_den}"
        zf = (c1n * ln + z1 * ld * c1d) / (ld * c1d)
        z_num = (c1n * ln + z1 * ld * c1d)
        z_den = (ld * c1d)
        z_gcd = gcd(z_num, z_den)
        z_num = z_num / z_gcd
        z_den = z_den / z_gcd
        z_fraction = f"{z_num} / {z_den}"
        # print(xf, yf, zf)
        return xf, yf, zf, x_fraction, y_fraction, z_fraction


def fop(x1, y1, z1, x2, y2, z2, x3, y3, z3):
    # print("--------fop--------")
    x1 = eval(tte(x1))
    x2 = eval(tte(x2))
    x3 = eval(tte(x3))
    y1 = eval(tte(y1))
    y2 = eval(tte(y2))
    y3 = eval(tte(y3))
    z1 = eval(tte(z1))
    z2 = eval(tte(z2))
    z3 = eval(tte(z3))
    a = (x1 - x2)
    b = (y1 - y2)
    c = (z1 - z2)
    # print("DR for fop", a, b, c)
    ln = 0
    ld = 0
    if a == b == c == 0:
        ln = 0
        # print("2nd lambda", ln)
    else:
        ln = (a * (x3 - x1) + b * (y3 - y1) + c * (z3 - z1))
        ld = (a * a + b * b + c * c)
        # print("1st lambda", ln,"/",ld)

    # x = (a*ln+x1*ld)/ld
    # y = (b*ln+y1*ld)/ld
    # z = (c*ln+z1*ld)/ld
    xn = (a * ln + x1 * ld)
    yn = (b * ln + y1 * ld)
    zn = (c * ln + z1 * ld)
    xd, yd, zd, = ld, ld, ld

    return xn, xd, yn, yd, zn, zd


def perimeter_3d(x1, y1, z1, x2, y2, z2, x3, y3, z3):
    x1 = eval(tte(x1))
    x2 = eval(tte(x2))
    x3 = eval(tte(x3))

    y1 = eval(tte(y1))
    y2 = eval(tte(y2))
    y3 = eval(tte(y3))

    z1 = eval(tte(z1))
    z2 = eval(tte(z2))
    z3 = eval(tte(z3))

    a = math.sqrt((x2 - x3) ** 2 + (y2 - y3) ** 2 + (z2 - z3) ** 2)
    b = math.sqrt((x1 - x3) ** 2 + (y1 - y3) ** 2 + (z1 - z3) ** 2)
    c = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)
    peri = a + b + c
    return peri


def perimeter_2d(x1, y1, x2, y2, x3, y3):
    z1, z2, z3 = "0", "0", "0"
    return perimeter_3d(x1, y1, z1, x2, y2, z2, x3, y3, z3)


def area_3d(x1, y1, z1, x2, y2, z2, x3, y3, z3):
    x1 = eval(tte(x1))
    x2 = eval(tte(x2))
    x3 = eval(tte(x3))
    y1 = eval(tte(y1))
    y2 = eval(tte(y2))
    y3 = eval(tte(y3))
    z1 = eval(tte(z1))
    z2 = eval(tte(z2))
    z3 = eval(tte(z3))

    i = (y1 - y2) * (z1 - z3) - (y1 - y3) * (z1 - z2)
    j = (x1 - x3) * (z1 - z2) - (x1 - x2) * (z1 - z3)
    k = (x1 - x2) * (y1 - y3) - (x1 - x3) * (y1 - y2)

    sq_sum = i * i + j * j + k * k
    ar = 1 / 2 * math.sqrt(sq_sum)
    return ar


def area_2d(x1, y1, x2, y2, x3, y3):
    x1 = eval(tte(x1))
    x2 = eval(tte(x2))
    x3 = eval(tte(x3))
    y1 = eval(tte(y1))
    y2 = eval(tte(y2))
    y3 = eval(tte(y3))
    ar = abs(x1 * y2 - x2 * y1 + x2 * y3 - x3 * y2 + x3 * y1 - x1 * y3)
    return ar / 2


class Centroid_3d:
    def __init__(self, x1, y1, z1, x2, y2, z2, x3, y3, z3):
        self.x1 = eval(tte(x1))
        self.y1 = eval(tte(y1))
        self.x2 = eval(tte(x2))

        self.y2 = eval(tte(y2))
        self.x3 = eval(tte(x3))
        self.y3 = eval(tte(y3))

        self.z1 = eval(tte(z1))
        self.z2 = eval(tte(z2))
        self.z3 = eval(tte(z3))

        self.x = (self.x1 + self.x2 + self.x3) / 3
        self.y = (self.y1 + self.y2 + self.y3) / 3
        self.y = (self.z1 + self.z2 + self.z3) / 3


class Centroid_2d:
    def __init__(self, x1, y1, x2, y2, x3, y3):
        self.x1 = eval(tte(x1))
        self.y1 = eval(tte(y1))
        self.x2 = eval(tte(x2))
        self.y2 = eval(tte(y2))
        self.x3 = eval(tte(x3))
        self.y3 = eval(tte(y3))
        self.x = (self.x1 + self.x2 + self.x3) / 3
        self.y = (self.y1 + self.y2 + self.y3) / 3


class Circumcentre_3d:
    def __init__(self, x1, y1, z1, x2, y2, z2, x3, y3, z3):
        self.x1 = eval(tte(x1))
        self.x2 = eval(tte(x2))
        self.x3 = eval(tte(x3))

        self.y1 = eval(tte(y1))
        self.y2 = eval(tte(y2))
        self.y3 = eval(tte(y3))

        self.z1 = eval(tte(z1))
        self.z2 = eval(tte(z2))
        self.z3 = eval(tte(z3))

        if self.x1 == self.x2 == self.x3 or self.y1 == self.y2 == self.y3 or self.z1 == self.z2 == self.z3:
            self.x = "∞"
            self.y = "∞"
            self.z = "∞"
            self.radius = "∞"
            self.radius_fraction = "∞"

        elif self.x1 == self.x2 == self.x3 == self.y1 == self.y2 == self.y3 == self.z1 == self.z2 == self.z3:
            self.x = "NaN"
            self.y = "NaN"
            self.z = "NaN"
            self.radius = "NaN"
            self.radius_fraction = "NaN"

        else:
            self.m = (self.y1 - self.y2) * (self.z2 - self.z3) - (self.y2 - self.y3) * (self.z1 - self.z2)
            self.n = -1 * ((self.x1 - self.x2) * (self.z2 - self.z3) - (self.x2 - self.x3) * (self.z1 - self.z2))
            self.o = (self.x1 - self.x2) * (self.y2 - self.y3) - (self.x2 - self.x3) * (self.y1 - self.y2)

            self.a1 = (self.z1 - self.z2) * self.n - (self.y1 - self.y2) * self.o
            self.b1 = self.o * (self.x1 - self.x2) - (self.z1 - self.z2) * self.m
            self.c1 = (self.y1 - self.y2) * self.m - (self.x1 - self.x2) * self.n

            self.a2 = (self.z3 - self.z2) * self.n - (self.y3 - self.y2) * self.o
            self.b2 = (self.x3 - self.x2) * self.o - (self.z2 - self.z2) * self.m
            self.c2 = (self.y3 - self.y2) * self.m - (self.x3 - self.x2) * self.n

            self.l = (self.a2 * (self.y1 - self.y3) + self.b2 * (self.x3 - self.x1)) / (
                    2 * (self.a1 * self.b2 - self.a2 * self.b1))
            self.x = self.a1 * self.l + (self.x1 + self.x2) / 2
            self.y = self.b1 * self.l + (self.y1 + self.y2) / 2
            self.z = self.c1 * self.l + (self.z1 + self.z2) / 2
            self.s1 = math.sqrt((self.x1 - self.x2) ** 2 + (self.y1 - self.y2) ** 2 + (self.z1 - self.z2) ** 2)
            self.s2 = math.sqrt((self.x1 - self.x3) ** 2 + (self.y1 - self.y3) ** 2 + (self.z1 - self.z3) ** 2)
            self.s3 = math.sqrt((self.x3 - self.x2) ** 2 + (self.y3 - self.y2) ** 2 + (self.z3 - self.z2) ** 2)
            self.ar = area_3d(self.x1, self.y1, self.z1, self.x2, self.y2, self.z2, self.x3, self.y3, self.z3)
            self.radius = self.s1 * self.s2 * self.s3 / 4 / self.ar
            self.radius_fraction = f"{self.s1 * self.s2 * self.s3}/{4 * self.ar}"


class Circumcentre_2d:

    def __init__(self, x1, y1, x2, y2, x3, y3):
        self.x1 = eval(tte(x1))
        self.y1 = eval(tte(y1))
        self.x2 = eval(tte(x2))
        self.y2 = eval(tte(y2))
        self.x3 = eval(tte(x3))
        self.y3 = eval(tte(y3))
        self.z1, self.z2, self.z3 = 0, 0, 0
        self.x, self.y, self.x_num, self.x_den, self.y_num, self.y_den, self.x_fraction, self.y_fraction, self.radius, self.radius_fraction = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

        if self.x1 == self.x2 == self.x3 and self.y1 == self.y2 == self.y3:
            self.x = eval(tte(f"({self.x1}^2+{self.y1}^2)/(2*{self.x1})"))
            self.x_num = eval(tte(f"({self.x1}^2+{self.y1}^2)"))
            self.xgcd = gcd(self.x_num, 2 * self.x1)
            self.x_num = self.x_num / self.xgcd
            self.x_den = 2 * self.x1 / self.xgcd
            self.x_fraction = f"{self.x_num}/{self.x_den}"
            self.y = eval(tte(f"({self.x1}^2+{self.y1}^2)/(2*{self.y1})"))
            self.y_num = eval(tte(f"({self.x1}^2+{self.y1}^2)"))
            self.ygcd = gcd(self.y_num, 2 * self.y1)
            self.y_num = self.y_num / self.ygcd
            self.y_den = 2 * self.x1 / self.ygcd
            self.y_fraction = f"{self.y_num}/{self.y_den}"
            self.radius = "Not defined"
            self.radius_fraction = "NaN"

        elif iscollinear(self.x1, self.x2, self.x3, self.y1, self.y2, self.y3) == True:

            self.x = "∞"
            self.x_fraction = "∞"

            self.y = "∞"
            self.y_fraction = "∞"
            self.radius = "∞"
            self.radius_fraction = "∞"

        else:
            cir_2d_from_3d = Circumcentre_3d(self.x1, self.y1, 0, self.x2, self.y2, 0, self.x3, self.y3, 0)
            self.x = cir_2d_from_3d.x
            self.y = cir_2d_from_3d.y
            self.z = cir_2d_from_3d.z
            self.s1 = math.sqrt((self.x1 - self.x2) ** 2 + (self.y1 - self.y2) ** 2)
            self.s2 = math.sqrt((self.x1 - self.x3) ** 2 + (self.y1 - self.y3) ** 2)
            self.s3 = math.sqrt((self.x3 - self.x2) ** 2 + (self.y3 - self.y2) ** 2)
            self.ar = area_2d(self.x1, self.y1, self.x2, self.y2, self.x3, self.y3)
            self.radius = self.s1 * self.s2 * self.s3 / 4 / self.ar
            self.radius_fraction = f"{self.s1 * self.s2 * self.s3}/({4 * self.ar}"


class Excentre_3d:
    def __init__(self, x1, y1, z1, x2, y2, z2, x3, y3, z3):
        self.x1 = eval(tte(x1))
        self.x2 = eval(tte(x2))
        self.x3 = eval(tte(x3))

        self.y1 = eval(tte(y1))
        self.y2 = eval(tte(y2))
        self.y3 = eval(tte(y3))

        self.z1 = eval(tte(z1))
        self.z2 = eval(tte(z2))
        self.z3 = eval(tte(z3))

        self.a = math.sqrt((self.x2 - self.x3) ** 2 + (self.y2 - self.y3) ** 2 + (self.z2 - self.z3) ** 2)
        self.b = math.sqrt((self.x1 - self.x3) ** 2 + (self.y1 - self.y3) ** 2 + (self.z1 - self.z3) ** 2)
        self.c = math.sqrt((self.x2 - self.x1) ** 2 + (self.y2 - self.y1) ** 2 + (self.z2 - self.z1) ** 2)
        self.semiperi = (self.a + self.b + self.c) / 2
        self.p1 = -1 * self.a + self.b + self.c
        self.p2 = self.a - self.b + self.c
        self.p3 = self.a + self.b - self.c

        if self.x1 == self.x2 == self.x3 and self.y1 == self.y2 == self.y3 and self.z1 == self.z2 == self.z3:
            self.x = self.x1
            self.y = self.y1
            self.z = self.z1
            self.radius = "∞"
            self.radius_fraction = "∞"

        else:
            self.xa = (-1 * self.a * self.x1 + self.b * self.x2 + self.c * self.x3) / self.p1
            self.xa_fraction = f"{(-1 * self.a * self.x1 + self.b * self.x2 + self.c * self.x3)}/{self.p1}"

            self.xb = (self.a * self.x1 - self.b * self.x2 + self.c * self.x3) / self.p2
            self.xb_fraction = f"{(self.a * self.x1 - self.b * self.x2 + self.c * self.x3)}/{self.p2}"

            self.xc = (self.a * self.x1 + self.b * self.x2 - self.c * self.x3) / self.p3
            self.xc_fraction = f"{(self.a * self.x1 + self.b * self.x2 - self.c * self.x3)}/{self.p3}"

            self.ya = (-1 * self.a * self.y1 + self.b * self.y2 + self.c * self.y3) / self.p1
            self.ya_fraction = f"{(-1 * self.a * self.y1 + self.b * self.y2 + self.c * self.y3)}/{self.p1}"

            self.yb = (self.a * self.y1 - self.b * self.y2 + self.c * self.y3) / self.p2
            self.yb_fraction = f"{(self.a * self.y1 - self.b * self.y2 + self.c * self.y3)}/{self.p2}"

            self.yc = (self.a * self.y1 + self.b * self.y2 - self.c * self.y3) / self.p3
            self.yc_fraction = f"{(self.a * self.y1 + self.b * self.y2 - self.c * self.y3)}/{self.p3}"

            self.za = (-1 * self.a * self.z1 + self.b * self.z2 + self.c * self.z3) / self.p1
            self.za_fraction = f"{(-1 * self.a * self.y1 + self.b * self.y2 + self.c * self.y3)}/{self.p1}"

            self.zb = (self.a * self.z1 - self.b * self.z2 + self.c * self.z3) / self.p2
            self.zb_fraction = f"{(self.a * self.y1 - self.b * self.y2 + self.c * self.y3)}/{self.p2}"

            self.zc = (self.a * self.z1 + self.b * self.z2 - self.c * self.z3) / self.p3
            self.zc_fraction = f"{(self.a * self.y1 + self.b * self.y2 - self.c * self.y3)}/{self.p3}"

            self.ar = area_3d(self.x1, self.y1, self.z1, self.x2, self.y2, self.z2, self.x3, self.y3, self.z3)
            self.radius1 = self.ar / (self.semiperi - self.a)
            self.radius2 = self.ar / (self.semiperi - self.b)
            self.radius3 = self.ar / (self.semiperi - self.c)
            if self.radius1 != 0:
                self.radius_fraction = f"{self.ar}/{self.semiperi - self.a}"
            else:
                self.radius_fraction = "0"
            if self.radius2 != 0:
                self.radius_fraction = f"{self.ar}/{self.semiperi - self.b}"
            else:
                self.radius_fraction = "0"
            if self.radius3 != 0:
                self.radius_fraction = f"{self.ar}/{self.semiperi - self.c}"
            else:
                self.radius_fraction = "0"


class Excentre_2d:
    def __init__(self, x1, y1, x2, y2, x3, y3):
        self.x1 = eval(tte(x1))
        self.x2 = eval(tte(x2))
        self.x3 = eval(tte(x3))

        self.y1 = eval(tte(y1))
        self.y2 = eval(tte(y2))
        self.y3 = eval(tte(y3))

        self.z1 = 0
        self.z2 = 0
        self.z3 = 0

        self.a = math.sqrt((self.x2 - self.x3) ** 2 + (self.y2 - self.y3) ** 2 + (self.z2 - self.z3) ** 2)
        self.b = math.sqrt((self.x1 - self.x3) ** 2 + (self.y1 - self.y3) ** 2 + (self.z1 - self.z3) ** 2)
        self.c = math.sqrt((self.x2 - self.x1) ** 2 + (self.y2 - self.y1) ** 2 + (self.z2 - self.z1) ** 2)
        self.semiperi = (self.a + self.b + self.c) / 2
        self.p1 = -1 * self.a + self.b + self.c
        self.p2 = self.a - self.b + self.c
        self.p3 = self.a + self.b - self.c

        if self.x1 == self.x2 == self.x3 and self.y1 == self.y2 == self.y3 and self.z1 == self.z2 == self.z3:
            self.x = self.x1
            self.y = self.y1
            self.z = self.z1
            self.radius = "∞"
            self.radius_fraction = "∞"

        else:
            self.xa = (-1 * self.a * self.x1 + self.b * self.x2 + self.c * self.x3) / self.p1
            self.xa_fraction = f"{(-1 * self.a * self.x1 + self.b * self.x2 + self.c * self.x3)}/{self.p1}"

            self.xa = (self.a * self.x1 - self.b * self.x2 + self.c * self.x3) / self.p2
            self.xa_fraction = f"{(self.a * self.x1 - self.b * self.x2 + self.c * self.x3)}/{self.p2}"

            self.xb = (self.a * self.x1 + self.b * self.x2 - self.c * self.x3) / self.p3
            self.xb_fraction = f"{(self.a * self.x1 + self.b * self.x2 - self.c * self.x3)}/{self.p3}"

            self.ya = (-1 * self.a * self.y1 + self.b * self.y2 + self.c * self.y3) / self.p1
            self.ya_fraction = f"{(-1 * self.a * self.y1 + self.b * self.y2 + self.c * self.y3)}/{self.p1}"

            self.yb = (self.a * self.y1 - self.b * self.y2 + self.c * self.y3) / self.p2
            self.yb_fraction = f"{(self.a * self.y1 - self.b * self.y2 + self.c * self.y3)}/{self.p2}"

            self.yc = (self.a * self.y1 + self.b * self.y2 - self.c * self.y3) / self.p3
            self.yc_fraction = f"{(self.a * self.y1 + self.b * self.y2 - self.c * self.y3)}/{self.p3}"

            self.za = (-1 * self.a * self.z1 + self.b * self.z2 + self.c * self.z3) / self.p1
            self.za_fraction = f"{(-1 * self.a * self.y1 + self.b * self.y2 + self.c * self.y3)}/{self.p1}"

            self.zb = (self.a * self.z1 - self.b * self.z2 + self.c * self.z3) / self.p2
            self.zb_fraction = f"{(self.a * self.y1 - self.b * self.y2 + self.c * self.y3)}/{self.p2}"

            self.zc = (self.a * self.z1 + self.b * self.z2 - self.c * self.z3) / self.p3
            self.zc_fraction = f"{(self.a * self.y1 + self.b * self.y2 - self.c * self.y3)}/{self.p3}"

            self.ar = area_3d(self.x1, self.y1, self.z1, self.x2, self.y2, self.z2, self.x3, self.y3, self.z3)
            self.radius1 = self.ar / (self.semiperi - self.a)
            self.radius2 = self.ar / (self.semiperi - self.b)
            self.radius3 = self.ar / (self.semiperi - self.c)
            if self.radius1 != 0:
                self.radius_fraction = f"{self.ar}/{self.semiperi - self.a}"
            else:
                self.radius_fraction = "0"
            if self.radius2 != 0:
                self.radius_fraction = f"{self.ar}/{self.semiperi - self.b}"
            else:
                self.radius_fraction = "0"
            if self.radius3 != 0:
                self.radius_fraction = f"{self.ar}/{self.semiperi - self.c}"
            else:
                self.radius_fraction = "0"


class Incentre_3d:
    def __init__(self, x1, y1, z1, x2, y2, z2, x3, y3, z3):
        self.x1 = eval(tte(x1))
        self.x2 = eval(tte(x2))
        self.x3 = eval(tte(x3))

        self.y1 = eval(tte(y1))
        self.y2 = eval(tte(y2))
        self.y3 = eval(tte(y3))

        self.z1 = eval(tte(z1))
        self.z2 = eval(tte(z2))
        self.z3 = eval(tte(z3))
        self.a = math.sqrt((self.x2 - self.x3) ** 2 + (self.y2 - self.y3) ** 2 + (self.z2 - self.z3) ** 2)
        self.b = math.sqrt((self.x1 - self.x3) ** 2 + (self.y1 - self.y3) ** 2 + (self.z1 - self.z3) ** 2)
        self.c = math.sqrt((self.x2 - self.x1) ** 2 + (self.y2 - self.y1) ** 2 + (self.z2 - self.z1) ** 2)
        self.perimeter = self.a + self.b + self.c

        if self.x1 == self.x2 == self.x3 and self.y1 == self.y2 == self.y3 and self.z1 == self.z2 == self.z3:
            self.x = self.x1
            self.y = self.y1
            self.z = self.z1
            self.radius = 0
            self.radius_fraction = "0"

        else:
            self.x = (self.a * self.x1 + self.b * self.x2 + self.c * self.x3) / self.perimeter
            self.x_fraction = f"{(self.a * self.x1 + self.b * self.x2 + self.c * self.x3)}/{self.perimeter}"
            self.y = (self.a * self.y1 + self.b * self.y2 + self.c * self.y3) / (self.a + self.b + self.c)
            self.y_fraction = f"{(self.a * self.y1 + self.b * self.y2 + self.c * self.y3)}/{self.perimeter}"
            self.z = (self.a * self.z1 + self.b * self.z2 + self.c * self.z3) / self.perimeter
            self.z_fraction = f"{(self.a * self.y1 + self.b * self.y2 + self.c * self.y3)}/{self.perimeter}"
            self.ar = area_3d(self.x1, self.y1, self.z1, self.x2, self.y2, self.z2, self.x3, self.y3, self.z3)
            self.radius = 2 * self.ar / self.perimeter
            if self.radius != 0:
                self.radius_fraction = f"{2 * self.ar}/{self.perimeter}"
            else:
                self.radius_fraction = "0"


class Incentre_2d:
    def __int__(self, x1, y1, x2, y2, x3, y3):
        self.x1 = eval(tte(x1))
        self.x2 = eval(tte(x2))
        self.x3 = eval(tte(x3))

        self.y1 = eval(tte(y1))
        self.y2 = eval(tte(y2))
        self.y3 = eval(tte(y3))

        self.z1 = 0
        self.z2 = 0
        self.z3 = 0
        self.a = math.sqrt((self.x2 - self.x3) ** 2 + (self.y2 - self.y3) ** 2 + (self.z2 - self.z3) ** 2)
        self.b = math.sqrt((self.x1 - self.x3) ** 2 + (self.y1 - self.y3) ** 2 + (self.z1 - self.z3) ** 2)
        self.c = math.sqrt((self.x2 - self.x1) ** 2 + (self.y2 - self.y1) ** 2 + (self.z2 - self.z1) ** 2)
        self.perimeter = self.a + self.b + self.c

        if self.x1 == self.x2 == self.x3 and self.y1 == self.y2 == self.y3 and self.z1 == self.z2 == self.z3:
            self.x = self.x1
            self.y = self.y1
            self.z = self.z1
            self.radius = 0
            self.radius_fraction = "0"

        else:
            self.x = (self.a * self.x1 + self.b * self.x2 + self.c * self.x3) / self.perimeter
            self.x_fraction = f"{(self.a * self.x1 + self.b * self.x2 + self.c * self.x3)}/{self.perimeter}"
            self.y = (self.a * self.y1 + self.b * self.y2 + self.c * self.y3) / (self.a + self.b + self.c)
            self.y_fraction = f"{(self.a * self.y1 + self.b * self.y2 + self.c * self.y3)}/{self.perimeter}"
            self.z = (self.a * self.z1 + self.b * self.z2 + self.c * self.z3) / self.perimeter
            self.z_fraction = f"{(self.a * self.y1 + self.b * self.y2 + self.c * self.y3)}/{self.perimeter}"
            self.ar = area_3d(self.x1, self.y1, self.z1, self.x2, self.y2, self.z2, self.x3, self.y3, self.z3)
            self.radius = 2 * self.ar / self.perimeter
            if self.radius != 0:
                self.radius_fraction = f"{2 * self.ar}/{self.perimeter}"
            else:
                self.radius_fraction = "0"


class Orthocentre_3d:
    def __init__(self, x1, y1, z1, x2, y2, z2, x3, y3, z3):
        self.x1 = eval(tte(x1))
        self.x2 = eval(tte(x2))
        self.x3 = eval(tte(x3))
        self.y1 = eval(tte(y1))
        self.y2 = eval(tte(y2))
        self.y3 = eval(tte(y3))
        self.z1 = eval(tte(z1))
        self.z2 = eval(tte(z2))
        self.z3 = eval(tte(z3))

        self.x4n, self.x4d, self.y4n, self.y4d, self.z4n, self.z4d = fop(x1, y1, z1, x2, y2, z2, x3, y3, z3)
        self.x5n, self.x5d, self.y5n, self.y5d, self.z5n, self.z5d = fop(x2, y2, z2, x3, y3, z3, x1, y1, z1)
        # print("foot of perp", self.x4n/self.x4d, self.y4n/self.x4d, self.z4n/self.x4d)
        # print("foot of perp of another", self.x5n/self.x5d, self.y5n/self.y5d, self.z5n/self.z5d)

        self.a1n = (self.x4n - self.x3 * self.x4d)
        self.a1d = self.x4d
        self.b1n = (self.y4n - self.y3 * self.y4d)
        self.b1d = self.y4d
        self.c1n = (self.z4n - self.z3 * self.z4d)
        self.c1d = self.z4d
        # print("DR", self.a1n/self.a1d, self.b1n/self.b1d, self.c1n/self.c1d)

        self.a2n = (self.x5n - self.x1 * self.x5d)
        self.a2d = self.x5d
        self.b2n = (self.y5n - self.y1 * self.y5d)
        self.b2d = self.y5d
        self.c2n = (self.z5n - self.z1 * self.z5d)
        self.c2d = self.z5d
        # print("DR of another", self.a2n/self.a2d, self.b2n/self.b2d, self.c2n/self.c2d)
        self.x, self.y, self.z, self.x_fraction, self.y_fraction, self.z_fraction = intersect(str(self.x3),
                                                                                              str(self.y3),
                                                                                              str(self.z3),
                                                                                              str(self.x1),
                                                                                              str(self.y1),
                                                                                              str(self.z1),
                                                                                              str(self.a1n),
                                                                                              str(self.a1d),
                                                                                              str(self.b1n),
                                                                                              str(self.b1d),
                                                                                              str(self.c1n),
                                                                                              str(self.c1d),
                                                                                              str(self.a2n),
                                                                                              str(self.a2d),
                                                                                              str(self.b2n),
                                                                                              str(self.b2d),
                                                                                              str(self.c2n),
                                                                                              str(self.c2d)
                                                                                              )


class Orthocentre_2d:
    def __init__(self, x1, y1, x2, y2, x3, y3):
        self.x1 = eval(tte(x1))
        self.x2 = eval(tte(x2))
        self.x3 = eval(tte(x3))
        self.y1 = eval(tte(y1))
        self.y2 = eval(tte(y2))
        self.y3 = eval(tte(y3))
        self.z1 = 0
        self.z2 = 0
        self.z3 = 0

        self.x4n, self.x4d, self.y4n, self.y4d, self.z4n, self.z4d = fop(x1, y1, 0, x2, y2, 0, x3, y3, 0)
        self.x5n, self.x5d, self.y5n, self.y5d, self.z5n, self.z5d = fop(x2, y2, 0, x3, y3, 0, x1, y1, 0)
        # print("foot of perp", self.x4n/self.x4d, self.y4n/self.x4d, self.z4n/self.x4d)
        # print("foot of perp of another", self.x5n/self.x5d, self.y5n/self.y5d, self.z5n/self.z5d)

        self.a1n = (self.x4n - self.x3 * self.x4d)
        self.a1d = self.x4d
        self.b1n = (self.y4n - self.y3 * self.y4d)
        self.b1d = self.y4d
        self.c1n = (self.z4n - self.z3 * self.z4d)
        self.c1d = self.z4d
        # print("DR", self.a1n/self.a1d, self.b1n/self.b1d, self.c1n/self.c1d)

        self.a2n = (self.x5n - self.x1 * self.x5d)
        self.a2d = self.x5d
        self.b2n = (self.y5n - self.y1 * self.y5d)
        self.b2d = self.y5d
        self.c2n = (self.z5n - self.z1 * self.z5d)
        self.c2d = self.z5d
        # print("DR of another", self.a2n/self.a2d, self.b2n/self.b2d, self.c2n/self.c2d)
        self.x, self.y, self.z, self.x_fraction, self.y_fraction, self.z_fraction = intersect(str(self.x3),
                                                                                              str(self.y3),
                                                                                              str(self.z3),
                                                                                              str(self.x1),
                                                                                              str(self.y1),
                                                                                              str(self.z1),
                                                                                              str(self.a1n),
                                                                                              str(self.a1d),
                                                                                              str(self.b1n),
                                                                                              str(self.b1d),
                                                                                              str(self.c1n),
                                                                                              str(self.c1d),
                                                                                              str(self.a2n),
                                                                                              str(self.a2d),
                                                                                              str(self.b2n),
                                                                                              str(self.b2d),
                                                                                              str(self.c2n),
                                                                                              str(self.c2d))
