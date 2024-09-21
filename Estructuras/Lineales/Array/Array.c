#include <Python.h>
#include <stdlib.h>
#include <io.h>

extern int errno;

typedef struct {
    PyObject_HEAD
    PyObject** arr;
    long long length;
} Array;

static void Array_dealloc(Array* self) {
    for (int i = 0; i < self->length; i++) {
        Py_XDECREF(self->arr[i]);
    }
    free(self->arr);
    self->arr = NULL;
    if (errno) {
        PyErr_SetFromErrno(PyExc_MemoryError);
    }
    Py_TYPE(self)->tp_free((PyObject *) self);
}

static int Array_init(Array *self, PyObject *args, PyObject *kwds) {
    long long l;
    if (!PyArg_ParseTuple(args, "L", &l)) {
        PyErr_BadArgument();
        return -1;
    }
    if (l < 0) {
        PyErr_SetString(PyExc_ValueError, "Target length must be a positive integer");
        return -1;
    }
    self->arr = (PyObject**) malloc((size_t)l*sizeof(PyObject*));
    if (!self->arr) {
        PyErr_SetFromErrno(PyExc_MemoryError);
        return -1;
    }
    self->length = l;
    for (int i = 0; i < l; i++) {
        self->arr[i] = NULL;
    }
    return 0;
}

PyObject* ArrayGet(Array *self, PyObject * args) {
    long long index;
    if (!PyArg_ParseTuple(args, "L", &index)) {
        PyErr_BadArgument();
        return NULL;
    }
    if (index < 0) {
        PyErr_SetString(PyExc_ValueError, "Target index must be equal or bigger than 0");
        return NULL;
    }
    if (index >= self->length) {
        PyErr_SetString(PyExc_ValueError, "Target index must be less than array length");
        return NULL;
    }
    return self->arr[index];
}

PyObject* Array_Get_(Array *self, Py_ssize_t i) {
    if (i < 0) {
        PyErr_SetString(PyExc_ValueError, "Target index must be equal or bigger than 0");
        return NULL;
    }
    if (i >= self->length) {
        PyErr_SetString(PyExc_ValueError, "Target index must be less than array length");
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
        PyErr_SetString(PyExc_ValueError, "Target index must be equal or bigger than 0");
        return NULL;
    }
    if (index >= self->length) {
        PyErr_SetString(PyExc_ValueError, "Target index must be less than array length");
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
        PyErr_SetString(PyExc_ValueError, "Target index must be equal or bigger than 0");
        return -1;
    }
    if (i >= self->length) {
        PyErr_SetString(PyExc_ValueError, "Target index must be less than array length");
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

int Array_del_(Array *self, Py_ssize_t i) {
    if (i < 0) {
        PyErr_SetString(PyExc_ValueError, "Target index must be equal or bigger than 0");
        return -1;
    }
    if (i >= self->length) {
        PyErr_SetString(PyExc_ValueError, "Target index must be less than array length");
        return -1;
    }
    PyObject *temp = self->arr[i];
    self->arr[i] = NULL;
    Py_XDECREF(temp);

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
    {"get", (PyCFunction) ArrayGet, METH_FASTCALL, "Returns item at index"},
    {"set", (PyCFunction) ArraySet, METH_FASTCALL, "Sets item at index"},
    {"__getitem__", (PyCFunction) ArrayGet, METH_FASTCALL, "Returns item at index"},
    {"__setitem__", (PyCFunction) ArrayGet, METH_FASTCALL, "Sets item at index"},
    {NULL, NULL, 0, NULL}
};

static PyTypeObject ArrayType = {
    .ob_base = PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "Array.Array",
    .tp_doc = PyDoc_STR("Array class"),
    .tp_basicsize = sizeof(Array),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_new = PyType_GenericNew,
    .tp_dealloc = (destructor) Array_dealloc,
    .tp_init = (initproc) Array_init,
    .tp_methods = ArrayMethods,
    .tp_as_sequence = &ArraySeqMet
};

static PyModuleDef arrayModule = {
    .m_base = PyModuleDef_HEAD_INIT,
    .m_name = "Array",
    .m_doc = PyDoc_STR("array module. Contains an extention type"),
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