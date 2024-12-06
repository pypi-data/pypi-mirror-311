// Copyright (c) 2021 Patricio Cubillos
// Pyrat Bay is open-source software under the GNU GPL-2.0 license (see LICENSE)

#include <Python.h>
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <numpy/arrayobject.h>

#include "ind.h"
#include "constants.h"
//#include "utils.h"


PyDoc_STRVAR(
    _two_stream__doc__,
"Calculate the differences between consecutive elements of an array.\n\
                                              \n\
Parameters                                    \n\
----------                                    \n\
arr: 2D float ndarray                         \n\
   Input array to get the differences from.   \n\
                                              \n\
Returns                                       \n\
-------                                       \n\
diff: 1D float ndarray                        \n\
   Array wth differences.");


static PyObject *_two_stream(PyObject *self, PyObject *args){
    PyArrayObject *flux_down, *flux_up, *B, *Bp, *dtau, *trans;
    int nlayers, nwave, i, j;

    // Load inputs:
    if (!PyArg_ParseTuple(
            args,
            "OOOOOO",
            &flux_down, &flux_up, &B, &Bp, &dtau, &trans))
        return NULL;

    nlayers = (int)PyArray_DIM(flux_down,0);
    nwave = (int)PyArray_DIM(flux_down,1);


    for (j=0; j<nwave; j++){
        for (i=0; i<nlayers-1; i++)
            IND2d(flux_down,(i+1),j) =
                IND2d(trans,i,j) * IND2d(flux_down,i,j)
                + PI * IND2d(B,i,j) * (1.0-IND2d(trans,i,j))
                + PI * IND2d(Bp,i,j) * (
                      -2.0/3.0 * (1.0-exp(-IND2d(dtau,i,j)))
                      + IND2d(dtau,i,j) * (1.0-IND2d(trans,i,j)/3.0));

        IND2d(flux_up,(nlayers-1),j) += IND2d(flux_down,(nlayers-1),j);

        for (i=nlayers-2; i>=0; i--){
            IND2d(flux_up,i,j) =
                IND2d(trans,i,j) * IND2d(flux_up,(i+1),j)
                + PI * IND2d(B,(i+1),j) * (1.0-IND2d(trans,i,j))
                + PI * IND2d(Bp,i,j) * (
                      2.0/3.0 * (1.0-exp(-IND2d(dtau,i,j)))
                      - IND2d(dtau,i,j) * (1.0-IND2d(trans,i,j)/3.0));
        }
    }

    return Py_BuildValue("");
}


/* The module doc string    */
PyDoc_STRVAR(
    two_stream__doc__,
    "Wrapper for the Planck emission calculation.");

/* A list of all the methods defined by this module.                        */
static PyMethodDef two_stream_methods[] = {
    {"_two_stream", _two_stream, METH_VARARGS, _two_stream__doc__},
    {NULL, NULL, 0, NULL}  // sentinel
};


/* Module definition for Python 3.                                          */
static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "_two_stream",
    two_stream__doc__,
    -1,
    two_stream_methods
};

/* When Python 3 imports a C module named 'X' it loads the module           */
/* then looks for a method named "PyInit_"+X and calls it.                  */
PyObject *PyInit__two_stream (void) {
    PyObject *module = PyModule_Create(&moduledef);
    import_array();
    return module;
}

