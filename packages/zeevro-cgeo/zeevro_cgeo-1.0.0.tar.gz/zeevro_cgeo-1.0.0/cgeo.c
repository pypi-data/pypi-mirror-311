#include <Python.h>
#include <math.h>

#define PI 3.1415926535897932384626433832795
#define EARTH_RADIUS 6378.137  // km

#define RAD(deg) (PI * (deg / 180))

typedef struct
{
	double X;
	double Y;
} point;

static PyObject * great_circle_distance(PyObject * self, PyObject * args)
{
	double s_lat, s_lng, d_lat, d_lng;
	double sin_s_lat, cos_s_lat, sin_d_lat, cos_d_lat;
	double delta_lng, sin_delta_lng, cos_delta_lng;
	double ret;

	PyArg_ParseTuple(args, "dddd", &s_lat, &s_lng, &d_lat, &d_lng);

	Py_BEGIN_ALLOW_THREADS

	s_lat = RAD(s_lat);
	s_lng = RAD(s_lng);
	d_lat = RAD(d_lat);
	d_lng = RAD(d_lng);

	sin_s_lat = sin(s_lat);
	cos_s_lat = cos(s_lat);
	sin_d_lat = sin(d_lat);
	cos_d_lat = cos(d_lat);

	delta_lng = d_lng - s_lng;
	sin_delta_lng = sin(delta_lng);
	cos_delta_lng = cos(delta_lng);

	ret = (
		atan2(
			sqrt(
				pow((cos_d_lat * sin_delta_lng), 2) +
				pow((cos_s_lat * sin_d_lat - sin_s_lat * cos_d_lat * cos_delta_lng), 2)
			),
			sin_s_lat * sin_d_lat + cos_s_lat * cos_d_lat * cos_delta_lng
		)
		* EARTH_RADIUS
	);

	Py_END_ALLOW_THREADS

	return Py_BuildValue("d", ret);
}

static PyObject * point_inside_polygon(PyObject * self, PyObject * args)
{
	double x, y;
	PyObject * poly_tuple;
	PyObject * poly_point;
	point * poly;
	unsigned long long len;
	int i, j, c = 0;

	PyArg_ParseTuple(args, "ddO", &x, &y, &poly_tuple);

	len = PySequence_Size(poly_tuple);

	poly = malloc(len * sizeof(point));
	if (!poly)
	{
		PyErr_SetString(PyExc_MemoryError, "Failed allocating memory for polygon!");
		return NULL;
	}

	for (i = 0; i < len; i++)
	{
		poly_point = PySequence_GetItem(poly_tuple, i);

		poly[i].X = PyFloat_AsDouble(PySequence_GetItem(poly_point, 0));
		poly[i].Y = PyFloat_AsDouble(PySequence_GetItem(poly_point, 1));
	}

	Py_BEGIN_ALLOW_THREADS

	for (i = 0, j = len - 1; i < len; j = i++)
	{
		if (((poly[i].Y > y) != (poly[j].Y > y)) && (x < (poly[j].X - poly[i].X) * (y - poly[i].Y) / (poly[j].Y - poly[i].Y) + poly[i].X))
		{
			c = !c;
		}
	}

	free(poly);

	Py_END_ALLOW_THREADS

	if (c) Py_RETURN_TRUE;
	Py_RETURN_FALSE;
}

static PyMethodDef module_funcs[] = {
	{"great_circle_distance", (PyCFunction)great_circle_distance, METH_VARARGS, "great_circle_distance(s_lat, s_lng, d_lat, d_lng)"},
	{"point_inside_polygon", (PyCFunction)point_inside_polygon, METH_VARARGS, "point_inside_polygon(x, y, ((x, y), ...))"},
	{NULL, NULL, 0, NULL},
};

int exec_module(PyObject * module)
{
	return PyModule_AddFunctions(module, module_funcs);
}

static PyModuleDef_Slot module_slots[] = {
	{Py_mod_exec, exec_module},
#ifdef Py_MOD_PER_INTERPRETER_GIL_SUPPORTED
	{Py_mod_multiple_interpreters, Py_MOD_PER_INTERPRETER_GIL_SUPPORTED},
#endif
	{0, NULL},
};

static PyModuleDef module_definition = {
	PyModuleDef_HEAD_INIT,
	"_cgeo",
	"A module with geographic functions",
	0,
	NULL,
	module_slots,
};

PyMODINIT_FUNC PyInit__cgeo(void)
{
	return PyModuleDef_Init(&module_definition);
}
