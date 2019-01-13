from time import time

from matplotlib import pyplot
from numpy import array, zeros, linspace, dot, inf, sqrt, clip, abs, cross
from numpy.linalg import norm


class Object3D:
    def __init__(self, x, y, z, specular=1., diffuse=1., ambient=.05, reflection=1):
        self.position = array([x, y, z])
        self.specular = specular
        self.diffuse = diffuse
        self.ambient = ambient
        self.reflection = reflection


class Plane(Object3D):
    def __init__(self, x, y, z, normal,  red=1., green=1., blue=1., **kwargs):
        super(Plane, self).__init__(x, y, z, **kwargs)
        self.color = array([red, green, blue])
        self.normal = array(normal)

    def intersect(self, o, d):
        denom = dot(d, self.normal)
        if abs(denom) < 1e-6:
            return inf
        d = dot(self.position - o, self.normal) / denom
        if d < 0:
            return inf
        return d

    def get_normal(self, _):
        return self.normal[:]


class Light(Object3D):
    def __init__(self, x, y, z, color=None, **kwargs):
        super(Light, self).__init__(x=x, y=y, z=z, **kwargs)

        self.color = array(color) if type(color) is list else array([1., 1., 1.])


class Screen(object):
    def __init__(self, x0, y0, x1, y1):
        self.camera = camera
        self.coordinates = array([x0, y0, x1, y1])
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1


class Camera(Object3D):
    def __init__(self, x, y, z, pointing):
        if type(pointing) is not type(array([])):
            raise ValueError("Wrong pointging value format: {}".format(type(pointing)))
        super(Camera, self).__init__(x=x, y=y, z=z)
        self.pointing = pointing

    def _get_normalize(self):
        value = self.pointing - self.position
        value /= norm(self.pointing - self.position)
        return value

    @property
    def normalize(self):
        return self._get_normalize()


class Sphere(Object3D):
    def __init__(self, radius, x, y, z, red=1., green=1., blue=1., **kwargs):
        super(Sphere, self).__init__(x=x, y=y, z=z, **kwargs)
        self.color = array([red, green, blue])
        self.radius = radius

    def intersect(self, o, d):
        a = dot(d, d)
        os = o - self.position
        b = 2 * dot(d, os)
        c = dot(os, os) - self.radius * self.radius
        disc = b * b - 4 * a * c
        if disc > 0:
            dist_sqrt = sqrt(disc)
            q = (-b - dist_sqrt) / 2.0 if b < 0 else (-b + dist_sqrt) / 2.0
            t0 = q / a
            t1 = c / q
            t0, t1 = min(t0, t1), max(t0, t1)
            if t1 >= 0:
                return t1 if t0 < 0 else t0
        return inf

    def __getitem__(self, item):
        if item == 0:
            return self.position[2]
        raise KeyError

    def get_normal(self, m):
        value = m - self.position
        value /= norm(value)
        return value


class Image:
    def __init__(self, screen, camera, light, high, width, objects=None, max_depth=5):
        self.camera = camera
        self.light = light
        self.high = high
        self.screen = screen
        self.width = width
        self.objects = objects if type(objects) is list else []
        if objects is not None and type(objects) is not list:
            self.objects.append(objects)

        self.max_depth = max_depth

    @staticmethod
    def _get_normal(obj, m):
        return obj.get_normal(m)

    @staticmethod
    def _normalize(value):
        value /= norm(value)
        return value

    def add_object(self, object_3d):
        self.objects.append(object_3d)
        return object_3d

    def get_image(self):
        img = zeros((self.high, self.width, 3))
        for i, x in enumerate(linspace(screen.x0, screen.x1, width)):
            for j, y in enumerate(linspace(screen.y0, screen.y1, high)):
                self.camera.position[:2] = (x, y)
                ray_o, ray_d = self.camera.position, self.camera.normalize
                depth = 0
                col = [0., 0., 0.]
                reflection = 1
                while depth < self.max_depth:
                    traced = self.trace_ray(ray_o, ray_d)
                    if traced is not None:
                        normal, point, color, obj_reflection = traced
                        ray_o, ray_d = point + normal * .0001, self._normalize(ray_d - 2 * dot(ray_d, normal) * normal)
                        col += reflection * color
                        reflection *= obj_reflection
                    depth += 1
                img[self.high - j - 1, i] = clip(col, 0, 1)
        return img

    def trace_ray(self, ray_o, ray_d):
        t = inf
        temp_obj = None
        for obj in self.objects:
            t_obj = obj.intersect(ray_o, ray_d)
            if t_obj < t:
                temp_obj = obj
                t = t_obj
        if t == inf:
            return
        return  self._get_color(ray_o, ray_d, temp_obj, t)

    def _get_color(self, ray_o, ray_d, obj, t):
        point = ray_o + ray_d * t
        normal = self._get_normal(obj, point)
        vector_to_camera = self._normalize(self.camera.position - point)
        lights = self.light if type(self.light) is list else [self.light]
        colors = []
        for light in lights:
            if list(light.color) == [0., 0., 0.]:
                break
            vector_to_light = self._normalize(light.position - point)
            percentage = self._check_colisions(obj, point, normal, vector_to_light)
            color = obj.ambient
            color += obj.diffuse * max(dot(normal, vector_to_light), 0.) * obj.color
            temp = self._normalize(vector_to_light + vector_to_camera)
            color += obj.specular * max(dot(normal, temp), 0.) ** 50. * light.color
            colors.append(color * percentage)
        if not colors:
            return
        return normal, point, sum(colors), obj.reflection


    def _check_colisions(self, obj, point, normal, vector_to_light):
        for new_obj in self.objects:
            if new_obj == obj:
                continue
            colision = new_obj.intersect(point + normal * .0001, vector_to_light)
            if colision < inf:
                return 0.15
            colision = new_obj.intersect(point + normal * .00001, vector_to_light)
            if colision < inf:
                return 0.3
        return 1


if __name__ == '__main__':
    camera = Camera(x=0., y=0.35, z=-1., pointing=array([0., 0., 0.]))

    high = 200
    width = 200
    r = float(width) / high

    screen = Screen(-1, -1 / r + .25, 1, 1 / r + .25)

    light1 = Light(x=5., y=5., z=-5., color=[1., 1., 1.])
    light2 = Light(x=-5., y=5., z=-15., color=[.0, .0, .0])

    s1 = Sphere(x=.9, y=.1, z=2.5, radius=.9, red=1., green=0., blue=0., reflection=0.25)
    s2 = Sphere(x=-1., y=.1, z=4.25, radius=.9, red=0., green=0., blue=1., reflection=0.35)
    s3 = Sphere(x=-4., y=.1, z=5.5, radius=.9, red=0., green=1., blue=0., reflection=0.45)

    p1 = Plane(
        x=0., y=-.8, z=0.,
        normal=[0., 1., 0.],
        red=.75, green=.0, blue=.75,
        specular=.15, diffuse=.75, ambient=.1, reflection=1
    )

    image = Image(screen=screen, high=high, width=width, camera=camera, light=[light1, light2], max_depth=6)

    image.add_object(s1)
    image.add_object(s2)
    image.add_object(s3)
    image.add_object(p1)

    print("Computing...")
    time1 = time()
    img = image.get_image()
    print("Time {}min {}sec".format(round((time() - time1) / 60), round((time() - time1) % 60)))

    pyplot.imshow(img, origin='lower', interpolation='nearest')
    pyplot.show()
