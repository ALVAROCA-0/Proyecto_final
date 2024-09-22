//python extension
#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "structmember.h"

//Array libs
#include <stdlib.h>
#include <errno.h>

typedef struct {
    PyObject_VAR_HEAD
    PyObject** arr;
    long long length;
} Array;

static PyObject* Array_new(PyTypeObject* type, PyObject* args, PyObject* kwds) {
    Array* self;
    long long l;
    if (!PyArg_ParseTuple(args, "L", &l)) {
        PyErr_BadArgument();
        l = 0;
    }
    if (l < 0) {
        PyErr_SetString(PyExc_ValueError, "El valor length debe ser un entero positivo");
        l = 0;
    }
    self  = (Array *) type->tp_alloc(type, 0);
    if (self) {
        self->arr = (PyObject*)malloc(type->tp_itemsize*l);
        self->length = l;
        Py_SET_SIZE(self, l);
    }
    return self;
}

static int Array_init(Array *self, PyObject *args, PyObject *kwds) {
    for (int i = 0; i < self->length; i++) {
        self->arr[i] = NULL;
    }
    return 0;
}

static int Array_traverse(Array *self, visitproc visit, void *arg) {
    if (self->length > 0 && self->arr) {
        for (int i = 0; i < self->length; i++) {
            Py_VISIT(self->arr[i]);
        }
    }
    return 0;
}

static int Array_clear(Array* self) {
    if (self->length > 0 && self->arr) {
        for (int i = 0; i < self->length; i++) {
            Py_CLEAR(self->arr[i]);
        }
    }
    return 0;
}

static void Array_finalize(Array* self) {
    PyObject *err_type, *err_value, *err_traceback;
    PyErr_Fetch(&err_type, &err_value, &err_traceback);
    Array_clear(self);
    free(self->arr);
    self->arr = NULL;
    PyErr_Restore(err_type, err_value, err_traceback);
}

static void Array_dealloc(Array* self) {
    PyObject_GC_UnTrack(self);
    PyObject *err_type, *err_value, *err_traceback;
    PyErr_Fetch(&err_type, &err_value, &err_traceback);
    Py_SET_SIZE(self, 0);
    PyErr_Restore(err_type, err_value, err_traceback);
    Py_TYPE(self)->tp_free((PyObject *) self);
}


PyObject* ArrayGet(Array *self, PyObject * args) {
    long long index;
    if (!PyArg_ParseTuple(args, "L", &index)) {
        PyErr_BadArgument();
        return NULL;
    }
    if (index < 0) {
        PyErr_SetString(PyExc_ValueError, "Indice debe ser un entero positivo");
        return NULL;
    }
    if (index >= self->length) {
        PyErr_SetString(PyExc_ValueError, "Indice debe ser menor al largo del Array");
        return NULL;
    }
    return self->arr[index];
}

PyObject* Array_Get_(Array *self, Py_ssize_t i) {
    if (i < 0) {
        PyErr_SetString(PyExc_ValueError, "Indice debe ser un entero positivo");
        return NULL;
    }
    if (i >= self->length) {
        PyErr_SetString(PyExc_ValueError, "Indice debe ser menor al largo del Array");
        return NULL;
    }
    return self->arr[i];
}

PyObject* ArraySet(Array *self, PyObject * args) {
    long long index;
    PyObject *new_object, *temp;
    if (!PyArg_ParseTuple(args, "LO", &index, &new_object)) {
        PyErr_BadArgument();
        return NULL;
    }
    if (index < 0) {
        PyErr_SetString(PyExc_ValueError, "Indice debe ser un entero positivo");
        return NULL;
    }
    if (index >= self->length) {
        PyErr_SetString(PyExc_ValueError, "Indice debe ser menor al largo del Array");
        return NULL;
    }
    if (new_object) {
        temp = self->arr[index];
        Py_INCREF(new_object);
        self->arr[index] = new_object;
        Py_XDECREF(temp);
    }
    return Py_None;
}

int Array_Set_(Array *self, Py_ssize_t i, PyObject * v) {
    PyObject *temp;
    if (i < 0) {
        PyErr_SetString(PyExc_ValueError, "Indice debe ser un entero positivo");
        return -1;
    }
    if (i >= self->length) {
        PyErr_SetString(PyExc_ValueError, "Indice debe ser menor al largo del Array");
        return -1;
    }
    if (v) {
        temp = self->arr[i];
        Py_INCREF(v);
        self->arr[i] = v;
        Py_XDECREF(temp);
    }
    return 0;
}

Py_ssize_t ArrayLen(Array *self) {
    return self->length;
}

static PySequenceMethods ArraySeqMet = {
    .sq_length = (lenfunc) ArrayLen,
    .sq_item = (ssizeargfunc) Array_Get_,
    .sq_ass_item = (ssizeobjargproc) Array_Set_
};

static PyMethodDef ArrayMethods[] = {
    {"get", (PyCFunction) ArrayGet, METH_FASTCALL, "Retorna el item en el indice"},
    {"set", (PyCFunction) ArraySet, METH_FASTCALL, "Cambia el valor en el indice"},
    {NULL, NULL, 0, NULL}
};

static PyTypeObject ArrayType = {
    .ob_base         = PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name         = "Array.Array",
    .tp_doc          = PyDoc_STR("Array class"),
    .tp_basicsize    = sizeof(Array),
    .tp_itemsize     = sizeof(PyObject*),
    .tp_flags        = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE | Py_TPFLAGS_HAVE_GC,
    .tp_new          = (newfunc)Array_new,
    .tp_init         = (initproc) Array_init,
    .tp_dealloc      = (destructor) Array_dealloc,
    .tp_finalize     = (destructor) Array_finalize,
    .tp_traverse     = (traverseproc) Array_traverse,
    .tp_clear        = (inquiry) Array_clear,
    .tp_methods      = ArrayMethods,
    .tp_as_sequence  = &ArraySeqMet,
};

static PyModuleDef arrayModule = {
    .m_base = PyModuleDef_HEAD_INIT,
    .m_name = "Array",
    .m_doc = PyDoc_STR("modulo array. Contiene la clase Array"),
    .m_size = -1
};

PyMODINIT_FUNC PyInit_Array(void) {
    PyObject *m;
    if (PyType_Ready(&ArrayType) < 0)
        return NULL;
    
    m = PyModule_Create(&arrayModule);
    if (m == NULL)
        return NULL;
    
    Py_INCREF(&ArrayType);
    if (PyModule_AddObject(m, "Array", (PyObject *) &ArrayType) < 0) {
        Py_DECREF(&ArrayType);
        Py_DECREF(m);
        return NULL;
    }

    return m;
}