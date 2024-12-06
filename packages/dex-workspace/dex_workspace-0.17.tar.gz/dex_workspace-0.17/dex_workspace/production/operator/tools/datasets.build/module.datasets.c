/* Generated code for Python module 'datasets'
 * created by Nuitka version 2.5.4
 *
 * This code is in part copyright 2024 Kay Hayen.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include "nuitka/prelude.h"

#include "nuitka/unfreezing.h"

#include "__helpers.h"

/* The "module_datasets" is a Python object pointer of module type.
 *
 * Note: For full compatibility with CPython, every module variable access
 * needs to go through it except for cases where the module cannot possibly
 * have changed in the mean time.
 */

PyObject *module_datasets;
PyDictObject *moduledict_datasets;

/* The declarations of module constants used, if any. */
static PyObject *mod_consts[24];
#ifndef __NUITKA_NO_ASSERT__
static Py_hash_t mod_consts_hash[24];
#endif

static PyObject *module_filename_obj = NULL;

/* Indicator if this modules private constants were created yet. */
static bool constants_created = false;

/* Function to create module private constants. */
static void createModuleConstants(PyThreadState *tstate) {
    if (constants_created == false) {
        loadConstantsBlob(tstate, &mod_consts[0], UN_TRANSLATE("datasets"));
        constants_created = true;

#ifndef __NUITKA_NO_ASSERT__
        for (int i = 0; i < 24; i++) {
            mod_consts_hash[i] = DEEP_HASH(tstate, mod_consts[i]);
        }
#endif
    }
}

// We want to be able to initialize the "__main__" constants in any case.
#if 0
void createMainModuleConstants(PyThreadState *tstate) {
    createModuleConstants(tstate);
}
#endif

/* Function to verify module private constants for non-corruption. */
#ifndef __NUITKA_NO_ASSERT__
void checkModuleConstants_datasets(PyThreadState *tstate) {
    // The module may not have been used at all, then ignore this.
    if (constants_created == false) return;

    for (int i = 0; i < 24; i++) {
        assert(mod_consts_hash[i] == DEEP_HASH(tstate, mod_consts[i]));
        CHECK_OBJECT_DEEP(mod_consts[i]);
    }
}
#endif

// Helper to preserving module variables for Python3.11+
#if 5
#if PYTHON_VERSION >= 0x3c0
NUITKA_MAY_BE_UNUSED static uint32_t _Nuitka_PyDictKeys_GetVersionForCurrentState(PyInterpreterState *interp, PyDictKeysObject *dk)
{
    if (dk->dk_version != 0) {
        return dk->dk_version;
    }
    uint32_t result = interp->dict_state.next_keys_version++;
    dk->dk_version = result;
    return result;
}
#elif PYTHON_VERSION >= 0x3b0
static uint32_t _Nuitka_next_dict_keys_version = 2;

NUITKA_MAY_BE_UNUSED static uint32_t _Nuitka_PyDictKeys_GetVersionForCurrentState(PyDictKeysObject *dk)
{
    if (dk->dk_version != 0) {
        return dk->dk_version;
    }
    uint32_t result = _Nuitka_next_dict_keys_version++;
    dk->dk_version = result;
    return result;
}
#endif
#endif

// Accessors to module variables.
static PyObject *module_var_accessor_datasets_$$___file__(PyThreadState *tstate) {
#if 0
    PyObject *result;

#if PYTHON_VERSION < 0x3b0
    static uint64_t dict_version = 0;
    static PyObject *cache_value = NULL;

    if (moduledict_datasets->ma_version_tag == dict_version) {
        CHECK_OBJECT_X(cache_value);
        result = cache_value;
    } else {
        dict_version = moduledict_datasets->ma_version_tag;

        result = GET_STRING_DICT_VALUE(moduledict_datasets, (Nuitka_StringObject *)mod_consts[6]);
        cache_value = result;
    }
#else
    static uint32_t dict_keys_version = 0xFFFFFFFF;
    static Py_ssize_t cache_dk_index = 0;

    PyDictKeysObject *dk = moduledict_datasets->ma_keys;
    if (likely(DK_IS_UNICODE(dk))) {

#if PYTHON_VERSION >= 0x3c0
        uint32_t current_dk_version = _Nuitka_PyDictKeys_GetVersionForCurrentState(tstate->interp, dk);
#else
        uint32_t current_dk_version = _Nuitka_PyDictKeys_GetVersionForCurrentState(dk);
#endif

        if (current_dk_version != dict_keys_version) {
            dict_keys_version = current_dk_version;
            Py_hash_t hash = ((Nuitka_StringObject *)mod_consts[6])->_base._base.hash;
            assert(hash != -1);

            cache_dk_index = Nuitka_Py_unicodekeys_lookup_unicode(dk, mod_consts[6], hash);
        }

        if (cache_dk_index >= 0) {
            assert(dk->dk_kind != DICT_KEYS_SPLIT);

            PyDictUnicodeEntry *entries = DK_UNICODE_ENTRIES(dk);

            result = entries[cache_dk_index].me_value;

            if (unlikely(result == NULL)) {
                Py_hash_t hash = ((Nuitka_StringObject *)mod_consts[6])->_base._base.hash;
                assert(hash != -1);

                cache_dk_index = Nuitka_Py_unicodekeys_lookup_unicode(dk, mod_consts[6], hash);

                if (cache_dk_index >= 0) {
                    result = entries[cache_dk_index].me_value;
                }
            }
        } else {
            result = NULL;
        }
    } else {
        result = GET_STRING_DICT_VALUE(moduledict_datasets, (Nuitka_StringObject *)mod_consts[6]);
    }
#endif

#else
    PyObject *result = GET_STRING_DICT_VALUE(moduledict_datasets, (Nuitka_StringObject *)mod_consts[6]);
#endif

    if (unlikely(result == NULL)) {
        result = GET_STRING_DICT_VALUE(dict_builtin, (Nuitka_StringObject *)mod_consts[6]);
    }

    return result;
}

static PyObject *module_var_accessor_datasets_$$___spec__(PyThreadState *tstate) {
#if 0
    PyObject *result;

#if PYTHON_VERSION < 0x3b0
    static uint64_t dict_version = 0;
    static PyObject *cache_value = NULL;

    if (moduledict_datasets->ma_version_tag == dict_version) {
        CHECK_OBJECT_X(cache_value);
        result = cache_value;
    } else {
        dict_version = moduledict_datasets->ma_version_tag;

        result = GET_STRING_DICT_VALUE(moduledict_datasets, (Nuitka_StringObject *)mod_consts[23]);
        cache_value = result;
    }
#else
    static uint32_t dict_keys_version = 0xFFFFFFFF;
    static Py_ssize_t cache_dk_index = 0;

    PyDictKeysObject *dk = moduledict_datasets->ma_keys;
    if (likely(DK_IS_UNICODE(dk))) {

#if PYTHON_VERSION >= 0x3c0
        uint32_t current_dk_version = _Nuitka_PyDictKeys_GetVersionForCurrentState(tstate->interp, dk);
#else
        uint32_t current_dk_version = _Nuitka_PyDictKeys_GetVersionForCurrentState(dk);
#endif

        if (current_dk_version != dict_keys_version) {
            dict_keys_version = current_dk_version;
            Py_hash_t hash = ((Nuitka_StringObject *)mod_consts[23])->_base._base.hash;
            assert(hash != -1);

            cache_dk_index = Nuitka_Py_unicodekeys_lookup_unicode(dk, mod_consts[23], hash);
        }

        if (cache_dk_index >= 0) {
            assert(dk->dk_kind != DICT_KEYS_SPLIT);

            PyDictUnicodeEntry *entries = DK_UNICODE_ENTRIES(dk);

            result = entries[cache_dk_index].me_value;

            if (unlikely(result == NULL)) {
                Py_hash_t hash = ((Nuitka_StringObject *)mod_consts[23])->_base._base.hash;
                assert(hash != -1);

                cache_dk_index = Nuitka_Py_unicodekeys_lookup_unicode(dk, mod_consts[23], hash);

                if (cache_dk_index >= 0) {
                    result = entries[cache_dk_index].me_value;
                }
            }
        } else {
            result = NULL;
        }
    } else {
        result = GET_STRING_DICT_VALUE(moduledict_datasets, (Nuitka_StringObject *)mod_consts[23]);
    }
#endif

#else
    PyObject *result = GET_STRING_DICT_VALUE(moduledict_datasets, (Nuitka_StringObject *)mod_consts[23]);
#endif

    if (unlikely(result == NULL)) {
        result = GET_STRING_DICT_VALUE(dict_builtin, (Nuitka_StringObject *)mod_consts[23]);
    }

    return result;
}

static PyObject *module_var_accessor_datasets_$$_datasets_path(PyThreadState *tstate) {
#if 1
    PyObject *result;

#if PYTHON_VERSION < 0x3b0
    static uint64_t dict_version = 0;
    static PyObject *cache_value = NULL;

    if (moduledict_datasets->ma_version_tag == dict_version) {
        CHECK_OBJECT_X(cache_value);
        result = cache_value;
    } else {
        dict_version = moduledict_datasets->ma_version_tag;

        result = GET_STRING_DICT_VALUE(moduledict_datasets, (Nuitka_StringObject *)mod_consts[1]);
        cache_value = result;
    }
#else
    static uint32_t dict_keys_version = 0xFFFFFFFF;
    static Py_ssize_t cache_dk_index = 0;

    PyDictKeysObject *dk = moduledict_datasets->ma_keys;
    if (likely(DK_IS_UNICODE(dk))) {

#if PYTHON_VERSION >= 0x3c0
        uint32_t current_dk_version = _Nuitka_PyDictKeys_GetVersionForCurrentState(tstate->interp, dk);
#else
        uint32_t current_dk_version = _Nuitka_PyDictKeys_GetVersionForCurrentState(dk);
#endif

        if (current_dk_version != dict_keys_version) {
            dict_keys_version = current_dk_version;
            Py_hash_t hash = ((Nuitka_StringObject *)mod_consts[1])->_base._base.hash;
            assert(hash != -1);

            cache_dk_index = Nuitka_Py_unicodekeys_lookup_unicode(dk, mod_consts[1], hash);
        }

        if (cache_dk_index >= 0) {
            assert(dk->dk_kind != DICT_KEYS_SPLIT);

            PyDictUnicodeEntry *entries = DK_UNICODE_ENTRIES(dk);

            result = entries[cache_dk_index].me_value;

            if (unlikely(result == NULL)) {
                Py_hash_t hash = ((Nuitka_StringObject *)mod_consts[1])->_base._base.hash;
                assert(hash != -1);

                cache_dk_index = Nuitka_Py_unicodekeys_lookup_unicode(dk, mod_consts[1], hash);

                if (cache_dk_index >= 0) {
                    result = entries[cache_dk_index].me_value;
                }
            }
        } else {
            result = NULL;
        }
    } else {
        result = GET_STRING_DICT_VALUE(moduledict_datasets, (Nuitka_StringObject *)mod_consts[1]);
    }
#endif

#else
    PyObject *result = GET_STRING_DICT_VALUE(moduledict_datasets, (Nuitka_StringObject *)mod_consts[1]);
#endif

    if (unlikely(result == NULL)) {
        result = GET_STRING_DICT_VALUE(dict_builtin, (Nuitka_StringObject *)mod_consts[1]);
    }

    return result;
}

static PyObject *module_var_accessor_datasets_$$_dirname(PyThreadState *tstate) {
#if 0
    PyObject *result;

#if PYTHON_VERSION < 0x3b0
    static uint64_t dict_version = 0;
    static PyObject *cache_value = NULL;

    if (moduledict_datasets->ma_version_tag == dict_version) {
        CHECK_OBJECT_X(cache_value);
        result = cache_value;
    } else {
        dict_version = moduledict_datasets->ma_version_tag;

        result = GET_STRING_DICT_VALUE(moduledict_datasets, (Nuitka_StringObject *)mod_consts[12]);
        cache_value = result;
    }
#else
    static uint32_t dict_keys_version = 0xFFFFFFFF;
    static Py_ssize_t cache_dk_index = 0;

    PyDictKeysObject *dk = moduledict_datasets->ma_keys;
    if (likely(DK_IS_UNICODE(dk))) {

#if PYTHON_VERSION >= 0x3c0
        uint32_t current_dk_version = _Nuitka_PyDictKeys_GetVersionForCurrentState(tstate->interp, dk);
#else
        uint32_t current_dk_version = _Nuitka_PyDictKeys_GetVersionForCurrentState(dk);
#endif

        if (current_dk_version != dict_keys_version) {
            dict_keys_version = current_dk_version;
            Py_hash_t hash = ((Nuitka_StringObject *)mod_consts[12])->_base._base.hash;
            assert(hash != -1);

            cache_dk_index = Nuitka_Py_unicodekeys_lookup_unicode(dk, mod_consts[12], hash);
        }

        if (cache_dk_index >= 0) {
            assert(dk->dk_kind != DICT_KEYS_SPLIT);

            PyDictUnicodeEntry *entries = DK_UNICODE_ENTRIES(dk);

            result = entries[cache_dk_index].me_value;

            if (unlikely(result == NULL)) {
                Py_hash_t hash = ((Nuitka_StringObject *)mod_consts[12])->_base._base.hash;
                assert(hash != -1);

                cache_dk_index = Nuitka_Py_unicodekeys_lookup_unicode(dk, mod_consts[12], hash);

                if (cache_dk_index >= 0) {
                    result = entries[cache_dk_index].me_value;
                }
            }
        } else {
            result = NULL;
        }
    } else {
        result = GET_STRING_DICT_VALUE(moduledict_datasets, (Nuitka_StringObject *)mod_consts[12]);
    }
#endif

#else
    PyObject *result = GET_STRING_DICT_VALUE(moduledict_datasets, (Nuitka_StringObject *)mod_consts[12]);
#endif

    if (unlikely(result == NULL)) {
        result = GET_STRING_DICT_VALUE(dict_builtin, (Nuitka_StringObject *)mod_consts[12]);
    }

    return result;
}

static PyObject *module_var_accessor_datasets_$$_np(PyThreadState *tstate) {
#if 1
    PyObject *result;

#if PYTHON_VERSION < 0x3b0
    static uint64_t dict_version = 0;
    static PyObject *cache_value = NULL;

    if (moduledict_datasets->ma_version_tag == dict_version) {
        CHECK_OBJECT_X(cache_value);
        result = cache_value;
    } else {
        dict_version = moduledict_datasets->ma_version_tag;

        result = GET_STRING_DICT_VALUE(moduledict_datasets, (Nuitka_StringObject *)mod_consts[2]);
        cache_value = result;
    }
#else
    static uint32_t dict_keys_version = 0xFFFFFFFF;
    static Py_ssize_t cache_dk_index = 0;

    PyDictKeysObject *dk = moduledict_datasets->ma_keys;
    if (likely(DK_IS_UNICODE(dk))) {

#if PYTHON_VERSION >= 0x3c0
        uint32_t current_dk_version = _Nuitka_PyDictKeys_GetVersionForCurrentState(tstate->interp, dk);
#else
        uint32_t current_dk_version = _Nuitka_PyDictKeys_GetVersionForCurrentState(dk);
#endif

        if (current_dk_version != dict_keys_version) {
            dict_keys_version = current_dk_version;
            Py_hash_t hash = ((Nuitka_StringObject *)mod_consts[2])->_base._base.hash;
            assert(hash != -1);

            cache_dk_index = Nuitka_Py_unicodekeys_lookup_unicode(dk, mod_consts[2], hash);
        }

        if (cache_dk_index >= 0) {
            assert(dk->dk_kind != DICT_KEYS_SPLIT);

            PyDictUnicodeEntry *entries = DK_UNICODE_ENTRIES(dk);

            result = entries[cache_dk_index].me_value;

            if (unlikely(result == NULL)) {
                Py_hash_t hash = ((Nuitka_StringObject *)mod_consts[2])->_base._base.hash;
                assert(hash != -1);

                cache_dk_index = Nuitka_Py_unicodekeys_lookup_unicode(dk, mod_consts[2], hash);

                if (cache_dk_index >= 0) {
                    result = entries[cache_dk_index].me_value;
                }
            }
        } else {
            result = NULL;
        }
    } else {
        result = GET_STRING_DICT_VALUE(moduledict_datasets, (Nuitka_StringObject *)mod_consts[2]);
    }
#endif

#else
    PyObject *result = GET_STRING_DICT_VALUE(moduledict_datasets, (Nuitka_StringObject *)mod_consts[2]);
#endif

    if (unlikely(result == NULL)) {
        result = GET_STRING_DICT_VALUE(dict_builtin, (Nuitka_StringObject *)mod_consts[2]);
    }

    return result;
}


// The module code objects.
static PyCodeObject *code_objects_57e560191028aae078dcbd68ca30bf96;
static PyCodeObject *code_objects_d309e91b5b42057bd4797ffea108dfcc;
static PyCodeObject *code_objects_68d7d53b79b82b605c7954c7e95042a6;

static void createModuleCodeObjects(void) {
    module_filename_obj = MAKE_RELATIVE_PATH(mod_consts[18]); CHECK_OBJECT(module_filename_obj);
    code_objects_57e560191028aae078dcbd68ca30bf96 = MAKE_CODE_OBJECT(module_filename_obj, 1, CO_NOFREE, mod_consts[19], mod_consts[19], NULL, NULL, 0, 0, 0);
    code_objects_d309e91b5b42057bd4797ffea108dfcc = MAKE_CODE_OBJECT(module_filename_obj, 11, CO_OPTIMIZED | CO_NEWLOCALS | CO_NOFREE, mod_consts[17], mod_consts[17], mod_consts[20], NULL, 2, 0, 0);
    code_objects_68d7d53b79b82b605c7954c7e95042a6 = MAKE_CODE_OBJECT(module_filename_obj, 7, CO_OPTIMIZED | CO_NEWLOCALS | CO_NOFREE, mod_consts[15], mod_consts[15], mod_consts[21], NULL, 2, 0, 0);
}

// The module function declarations.
static PyObject *MAKE_FUNCTION_datasets$$$function__1_store_numpy(PyObject *annotations);


static PyObject *MAKE_FUNCTION_datasets$$$function__2_rename_file(PyObject *annotations);


// The module function definitions.
static PyObject *impl_datasets$$$function__1_store_numpy(PyThreadState *tstate, struct Nuitka_FunctionObject const *self, PyObject **python_pars) {
    // Preserve error status for checks
#ifndef __NUITKA_NO_ASSERT__
    NUITKA_MAY_BE_UNUSED bool had_error = HAS_ERROR_OCCURRED(tstate);
#endif

    // Local variable declarations.
    PyObject *par_array = python_pars[0];
    PyObject *par_name = python_pars[1];
    PyObject *var_file_path = NULL;
    struct Nuitka_FrameObject *frame_68d7d53b79b82b605c7954c7e95042a6;
    NUITKA_MAY_BE_UNUSED char const *type_description_1 = NULL;
    struct Nuitka_ExceptionPreservationItem exception_state = Empty_Nuitka_ExceptionPreservationItem;
    NUITKA_MAY_BE_UNUSED int exception_lineno = 0;
    NUITKA_MAY_BE_UNUSED nuitka_void tmp_unused;
    static struct Nuitka_FrameObject *cache_frame_68d7d53b79b82b605c7954c7e95042a6 = NULL;
    PyObject *tmp_return_value = NULL;
    struct Nuitka_ExceptionPreservationItem exception_keeper_name_1;
    NUITKA_MAY_BE_UNUSED int exception_keeper_lineno_1;

    // Actual function body.
    // Tried code:
    if (isFrameUnusable(cache_frame_68d7d53b79b82b605c7954c7e95042a6)) {
        Py_XDECREF(cache_frame_68d7d53b79b82b605c7954c7e95042a6);

#if _DEBUG_REFCOUNTS
        if (cache_frame_68d7d53b79b82b605c7954c7e95042a6 == NULL) {
            count_active_frame_cache_instances += 1;
        } else {
            count_released_frame_cache_instances += 1;
        }
        count_allocated_frame_cache_instances += 1;
#endif
        cache_frame_68d7d53b79b82b605c7954c7e95042a6 = MAKE_FUNCTION_FRAME(tstate, code_objects_68d7d53b79b82b605c7954c7e95042a6, module_datasets, sizeof(void *)+sizeof(void *)+sizeof(void *));
#if _DEBUG_REFCOUNTS
    } else {
        count_hit_frame_cache_instances += 1;
#endif
    }

    assert(cache_frame_68d7d53b79b82b605c7954c7e95042a6->m_type_description == NULL);
    frame_68d7d53b79b82b605c7954c7e95042a6 = cache_frame_68d7d53b79b82b605c7954c7e95042a6;

    // Push the new frame as the currently active one, and we should be exclusively
    // owning it.
    pushFrameStackCompiledFrame(tstate, frame_68d7d53b79b82b605c7954c7e95042a6);
    assert(Py_REFCNT(frame_68d7d53b79b82b605c7954c7e95042a6) == 2);

    // Framed code:
    {
        PyObject *tmp_assign_source_1;
        PyObject *tmp_called_value_1;
        PyObject *tmp_expression_value_1;
        PyObject *tmp_args_element_value_1;
        PyObject *tmp_args_element_value_2;
        tmp_expression_value_1 = IMPORT_HARD_POSIXPATH();
        assert(!(tmp_expression_value_1 == NULL));
        tmp_called_value_1 = LOOKUP_ATTRIBUTE(tstate, tmp_expression_value_1, mod_consts[0]);
        if (tmp_called_value_1 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 8;
            type_description_1 = "ooo";
            goto frame_exception_exit_1;
        }
        tmp_args_element_value_1 = module_var_accessor_datasets_$$_datasets_path(tstate);
        if (unlikely(tmp_args_element_value_1 == NULL)) {
            RAISE_CURRENT_EXCEPTION_NAME_ERROR(tstate, &exception_state, mod_consts[1]);
        }

        if (tmp_args_element_value_1 == NULL) {
            assert(HAS_EXCEPTION_STATE(&exception_state));

            Py_DECREF(tmp_called_value_1);

            exception_lineno = 8;
            type_description_1 = "ooo";
            goto frame_exception_exit_1;
        }
        CHECK_OBJECT(par_name);
        tmp_args_element_value_2 = par_name;
        frame_68d7d53b79b82b605c7954c7e95042a6->m_frame.f_lineno = 8;
        {
            PyObject *call_args[] = {tmp_args_element_value_1, tmp_args_element_value_2};
            tmp_assign_source_1 = CALL_FUNCTION_WITH_ARGS2(tstate, tmp_called_value_1, call_args);
        }

        Py_DECREF(tmp_called_value_1);
        if (tmp_assign_source_1 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 8;
            type_description_1 = "ooo";
            goto frame_exception_exit_1;
        }
        assert(var_file_path == NULL);
        var_file_path = tmp_assign_source_1;
    }
    {
        PyObject *tmp_called_instance_1;
        PyObject *tmp_call_result_1;
        PyObject *tmp_args_element_value_3;
        PyObject *tmp_args_element_value_4;
        tmp_called_instance_1 = module_var_accessor_datasets_$$_np(tstate);
        if (unlikely(tmp_called_instance_1 == NULL)) {
            RAISE_CURRENT_EXCEPTION_NAME_ERROR(tstate, &exception_state, mod_consts[2]);
        }

        if (tmp_called_instance_1 == NULL) {
            assert(HAS_EXCEPTION_STATE(&exception_state));



            exception_lineno = 9;
            type_description_1 = "ooo";
            goto frame_exception_exit_1;
        }
        CHECK_OBJECT(var_file_path);
        tmp_args_element_value_3 = var_file_path;
        CHECK_OBJECT(par_array);
        tmp_args_element_value_4 = par_array;
        frame_68d7d53b79b82b605c7954c7e95042a6->m_frame.f_lineno = 9;
        {
            PyObject *call_args[] = {tmp_args_element_value_3, tmp_args_element_value_4};
            tmp_call_result_1 = CALL_METHOD_WITH_ARGS2(
                tstate,
                tmp_called_instance_1,
                mod_consts[3],
                call_args
            );
        }

        if (tmp_call_result_1 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 9;
            type_description_1 = "ooo";
            goto frame_exception_exit_1;
        }
        Py_DECREF(tmp_call_result_1);
    }


    // Put the previous frame back on top.
    popFrameStack(tstate);

    goto frame_no_exception_1;
    frame_exception_exit_1:


    {
        PyTracebackObject *exception_tb = GET_EXCEPTION_STATE_TRACEBACK(&exception_state);
        if (exception_tb == NULL) {
            exception_tb = MAKE_TRACEBACK(frame_68d7d53b79b82b605c7954c7e95042a6, exception_lineno);
            SET_EXCEPTION_STATE_TRACEBACK(&exception_state, exception_tb);
        } else if (exception_tb->tb_frame != &frame_68d7d53b79b82b605c7954c7e95042a6->m_frame) {
            exception_tb = ADD_TRACEBACK(exception_tb, frame_68d7d53b79b82b605c7954c7e95042a6, exception_lineno);
            SET_EXCEPTION_STATE_TRACEBACK(&exception_state, exception_tb);
        }
    }

    // Attaches locals to frame if any.
    Nuitka_Frame_AttachLocals(
        frame_68d7d53b79b82b605c7954c7e95042a6,
        type_description_1,
        par_array,
        par_name,
        var_file_path
    );


    // Release cached frame if used for exception.
    if (frame_68d7d53b79b82b605c7954c7e95042a6 == cache_frame_68d7d53b79b82b605c7954c7e95042a6) {
#if _DEBUG_REFCOUNTS
        count_active_frame_cache_instances -= 1;
        count_released_frame_cache_instances += 1;
#endif
        Py_DECREF(cache_frame_68d7d53b79b82b605c7954c7e95042a6);
        cache_frame_68d7d53b79b82b605c7954c7e95042a6 = NULL;
    }

    assertFrameObject(frame_68d7d53b79b82b605c7954c7e95042a6);

    // Put the previous frame back on top.
    popFrameStack(tstate);

    // Return the error.
    goto try_except_handler_1;
    frame_no_exception_1:;
    tmp_return_value = Py_None;
    Py_INCREF(tmp_return_value);
    goto try_return_handler_1;
    NUITKA_CANNOT_GET_HERE("tried codes exits in all cases");
    return NULL;
    // Return handler code:
    try_return_handler_1:;
    CHECK_OBJECT(var_file_path);
    Py_DECREF(var_file_path);
    var_file_path = NULL;
    goto function_return_exit;
    // Exception handler code:
    try_except_handler_1:;
    exception_keeper_lineno_1 = exception_lineno;
    exception_lineno = 0;
    exception_keeper_name_1 = exception_state;
    INIT_ERROR_OCCURRED_STATE(&exception_state);

    Py_XDECREF(var_file_path);
    var_file_path = NULL;
    // Re-raise.
    exception_state = exception_keeper_name_1;
    exception_lineno = exception_keeper_lineno_1;

    goto function_exception_exit;
    // End of try:

    NUITKA_CANNOT_GET_HERE("Return statement must have exited already.");
    return NULL;

function_exception_exit:
    CHECK_OBJECT(par_array);
    Py_DECREF(par_array);
    CHECK_OBJECT(par_name);
    Py_DECREF(par_name);
    CHECK_EXCEPTION_STATE(&exception_state);
    RESTORE_ERROR_OCCURRED_STATE(tstate, &exception_state);

    return NULL;

function_return_exit:
   // Function cleanup code if any.
    CHECK_OBJECT(par_array);
    Py_DECREF(par_array);
    CHECK_OBJECT(par_name);
    Py_DECREF(par_name);

   // Actual function exit with return value, making sure we did not make
   // the error status worse despite non-NULL return.
   CHECK_OBJECT(tmp_return_value);
   assert(had_error || !HAS_ERROR_OCCURRED(tstate));
   return tmp_return_value;
}


static PyObject *impl_datasets$$$function__2_rename_file(PyThreadState *tstate, struct Nuitka_FunctionObject const *self, PyObject **python_pars) {
    // Preserve error status for checks
#ifndef __NUITKA_NO_ASSERT__
    NUITKA_MAY_BE_UNUSED bool had_error = HAS_ERROR_OCCURRED(tstate);
#endif

    // Local variable declarations.
    PyObject *par_old_name = python_pars[0];
    PyObject *par_new_name = python_pars[1];
    PyObject *var_old_file_path = NULL;
    PyObject *var_new_file_path = NULL;
    struct Nuitka_FrameObject *frame_d309e91b5b42057bd4797ffea108dfcc;
    NUITKA_MAY_BE_UNUSED char const *type_description_1 = NULL;
    struct Nuitka_ExceptionPreservationItem exception_state = Empty_Nuitka_ExceptionPreservationItem;
    NUITKA_MAY_BE_UNUSED int exception_lineno = 0;
    NUITKA_MAY_BE_UNUSED nuitka_void tmp_unused;
    static struct Nuitka_FrameObject *cache_frame_d309e91b5b42057bd4797ffea108dfcc = NULL;
    PyObject *tmp_return_value = NULL;
    struct Nuitka_ExceptionPreservationItem exception_keeper_name_1;
    NUITKA_MAY_BE_UNUSED int exception_keeper_lineno_1;

    // Actual function body.
    // Tried code:
    if (isFrameUnusable(cache_frame_d309e91b5b42057bd4797ffea108dfcc)) {
        Py_XDECREF(cache_frame_d309e91b5b42057bd4797ffea108dfcc);

#if _DEBUG_REFCOUNTS
        if (cache_frame_d309e91b5b42057bd4797ffea108dfcc == NULL) {
            count_active_frame_cache_instances += 1;
        } else {
            count_released_frame_cache_instances += 1;
        }
        count_allocated_frame_cache_instances += 1;
#endif
        cache_frame_d309e91b5b42057bd4797ffea108dfcc = MAKE_FUNCTION_FRAME(tstate, code_objects_d309e91b5b42057bd4797ffea108dfcc, module_datasets, sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *));
#if _DEBUG_REFCOUNTS
    } else {
        count_hit_frame_cache_instances += 1;
#endif
    }

    assert(cache_frame_d309e91b5b42057bd4797ffea108dfcc->m_type_description == NULL);
    frame_d309e91b5b42057bd4797ffea108dfcc = cache_frame_d309e91b5b42057bd4797ffea108dfcc;

    // Push the new frame as the currently active one, and we should be exclusively
    // owning it.
    pushFrameStackCompiledFrame(tstate, frame_d309e91b5b42057bd4797ffea108dfcc);
    assert(Py_REFCNT(frame_d309e91b5b42057bd4797ffea108dfcc) == 2);

    // Framed code:
    {
        PyObject *tmp_assign_source_1;
        PyObject *tmp_called_value_1;
        PyObject *tmp_expression_value_1;
        PyObject *tmp_args_element_value_1;
        PyObject *tmp_args_element_value_2;
        tmp_expression_value_1 = IMPORT_HARD_POSIXPATH();
        assert(!(tmp_expression_value_1 == NULL));
        tmp_called_value_1 = LOOKUP_ATTRIBUTE(tstate, tmp_expression_value_1, mod_consts[0]);
        if (tmp_called_value_1 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 12;
            type_description_1 = "oooo";
            goto frame_exception_exit_1;
        }
        tmp_args_element_value_1 = module_var_accessor_datasets_$$_datasets_path(tstate);
        if (unlikely(tmp_args_element_value_1 == NULL)) {
            RAISE_CURRENT_EXCEPTION_NAME_ERROR(tstate, &exception_state, mod_consts[1]);
        }

        if (tmp_args_element_value_1 == NULL) {
            assert(HAS_EXCEPTION_STATE(&exception_state));

            Py_DECREF(tmp_called_value_1);

            exception_lineno = 12;
            type_description_1 = "oooo";
            goto frame_exception_exit_1;
        }
        CHECK_OBJECT(par_old_name);
        tmp_args_element_value_2 = par_old_name;
        frame_d309e91b5b42057bd4797ffea108dfcc->m_frame.f_lineno = 12;
        {
            PyObject *call_args[] = {tmp_args_element_value_1, tmp_args_element_value_2};
            tmp_assign_source_1 = CALL_FUNCTION_WITH_ARGS2(tstate, tmp_called_value_1, call_args);
        }

        Py_DECREF(tmp_called_value_1);
        if (tmp_assign_source_1 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 12;
            type_description_1 = "oooo";
            goto frame_exception_exit_1;
        }
        assert(var_old_file_path == NULL);
        var_old_file_path = tmp_assign_source_1;
    }
    {
        PyObject *tmp_assign_source_2;
        PyObject *tmp_called_value_2;
        PyObject *tmp_expression_value_2;
        PyObject *tmp_args_element_value_3;
        PyObject *tmp_args_element_value_4;
        tmp_expression_value_2 = IMPORT_HARD_POSIXPATH();
        assert(!(tmp_expression_value_2 == NULL));
        tmp_called_value_2 = LOOKUP_ATTRIBUTE(tstate, tmp_expression_value_2, mod_consts[0]);
        if (tmp_called_value_2 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 13;
            type_description_1 = "oooo";
            goto frame_exception_exit_1;
        }
        tmp_args_element_value_3 = module_var_accessor_datasets_$$_datasets_path(tstate);
        if (unlikely(tmp_args_element_value_3 == NULL)) {
            RAISE_CURRENT_EXCEPTION_NAME_ERROR(tstate, &exception_state, mod_consts[1]);
        }

        if (tmp_args_element_value_3 == NULL) {
            assert(HAS_EXCEPTION_STATE(&exception_state));

            Py_DECREF(tmp_called_value_2);

            exception_lineno = 13;
            type_description_1 = "oooo";
            goto frame_exception_exit_1;
        }
        CHECK_OBJECT(par_new_name);
        tmp_args_element_value_4 = par_new_name;
        frame_d309e91b5b42057bd4797ffea108dfcc->m_frame.f_lineno = 13;
        {
            PyObject *call_args[] = {tmp_args_element_value_3, tmp_args_element_value_4};
            tmp_assign_source_2 = CALL_FUNCTION_WITH_ARGS2(tstate, tmp_called_value_2, call_args);
        }

        Py_DECREF(tmp_called_value_2);
        if (tmp_assign_source_2 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 13;
            type_description_1 = "oooo";
            goto frame_exception_exit_1;
        }
        assert(var_new_file_path == NULL);
        var_new_file_path = tmp_assign_source_2;
    }
    {
        PyObject *tmp_called_instance_1;
        PyObject *tmp_call_result_1;
        PyObject *tmp_args_element_value_5;
        PyObject *tmp_args_element_value_6;
        tmp_called_instance_1 = IMPORT_HARD_OS();
        assert(!(tmp_called_instance_1 == NULL));
        CHECK_OBJECT(var_old_file_path);
        tmp_args_element_value_5 = var_old_file_path;
        CHECK_OBJECT(var_new_file_path);
        tmp_args_element_value_6 = var_new_file_path;
        frame_d309e91b5b42057bd4797ffea108dfcc->m_frame.f_lineno = 14;
        {
            PyObject *call_args[] = {tmp_args_element_value_5, tmp_args_element_value_6};
            tmp_call_result_1 = CALL_METHOD_WITH_ARGS2(
                tstate,
                tmp_called_instance_1,
                mod_consts[4],
                call_args
            );
        }

        if (tmp_call_result_1 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 14;
            type_description_1 = "oooo";
            goto frame_exception_exit_1;
        }
        Py_DECREF(tmp_call_result_1);
    }


    // Put the previous frame back on top.
    popFrameStack(tstate);

    goto frame_no_exception_1;
    frame_exception_exit_1:


    {
        PyTracebackObject *exception_tb = GET_EXCEPTION_STATE_TRACEBACK(&exception_state);
        if (exception_tb == NULL) {
            exception_tb = MAKE_TRACEBACK(frame_d309e91b5b42057bd4797ffea108dfcc, exception_lineno);
            SET_EXCEPTION_STATE_TRACEBACK(&exception_state, exception_tb);
        } else if (exception_tb->tb_frame != &frame_d309e91b5b42057bd4797ffea108dfcc->m_frame) {
            exception_tb = ADD_TRACEBACK(exception_tb, frame_d309e91b5b42057bd4797ffea108dfcc, exception_lineno);
            SET_EXCEPTION_STATE_TRACEBACK(&exception_state, exception_tb);
        }
    }

    // Attaches locals to frame if any.
    Nuitka_Frame_AttachLocals(
        frame_d309e91b5b42057bd4797ffea108dfcc,
        type_description_1,
        par_old_name,
        par_new_name,
        var_old_file_path,
        var_new_file_path
    );


    // Release cached frame if used for exception.
    if (frame_d309e91b5b42057bd4797ffea108dfcc == cache_frame_d309e91b5b42057bd4797ffea108dfcc) {
#if _DEBUG_REFCOUNTS
        count_active_frame_cache_instances -= 1;
        count_released_frame_cache_instances += 1;
#endif
        Py_DECREF(cache_frame_d309e91b5b42057bd4797ffea108dfcc);
        cache_frame_d309e91b5b42057bd4797ffea108dfcc = NULL;
    }

    assertFrameObject(frame_d309e91b5b42057bd4797ffea108dfcc);

    // Put the previous frame back on top.
    popFrameStack(tstate);

    // Return the error.
    goto try_except_handler_1;
    frame_no_exception_1:;
    tmp_return_value = Py_None;
    Py_INCREF(tmp_return_value);
    goto try_return_handler_1;
    NUITKA_CANNOT_GET_HERE("tried codes exits in all cases");
    return NULL;
    // Return handler code:
    try_return_handler_1:;
    CHECK_OBJECT(var_old_file_path);
    Py_DECREF(var_old_file_path);
    var_old_file_path = NULL;
    CHECK_OBJECT(var_new_file_path);
    Py_DECREF(var_new_file_path);
    var_new_file_path = NULL;
    goto function_return_exit;
    // Exception handler code:
    try_except_handler_1:;
    exception_keeper_lineno_1 = exception_lineno;
    exception_lineno = 0;
    exception_keeper_name_1 = exception_state;
    INIT_ERROR_OCCURRED_STATE(&exception_state);

    Py_XDECREF(var_old_file_path);
    var_old_file_path = NULL;
    Py_XDECREF(var_new_file_path);
    var_new_file_path = NULL;
    // Re-raise.
    exception_state = exception_keeper_name_1;
    exception_lineno = exception_keeper_lineno_1;

    goto function_exception_exit;
    // End of try:

    NUITKA_CANNOT_GET_HERE("Return statement must have exited already.");
    return NULL;

function_exception_exit:
    CHECK_OBJECT(par_old_name);
    Py_DECREF(par_old_name);
    CHECK_OBJECT(par_new_name);
    Py_DECREF(par_new_name);
    CHECK_EXCEPTION_STATE(&exception_state);
    RESTORE_ERROR_OCCURRED_STATE(tstate, &exception_state);

    return NULL;

function_return_exit:
   // Function cleanup code if any.
    CHECK_OBJECT(par_old_name);
    Py_DECREF(par_old_name);
    CHECK_OBJECT(par_new_name);
    Py_DECREF(par_new_name);

   // Actual function exit with return value, making sure we did not make
   // the error status worse despite non-NULL return.
   CHECK_OBJECT(tmp_return_value);
   assert(had_error || !HAS_ERROR_OCCURRED(tstate));
   return tmp_return_value;
}



static PyObject *MAKE_FUNCTION_datasets$$$function__1_store_numpy(PyObject *annotations) {
    struct Nuitka_FunctionObject *result = Nuitka_Function_New(
        impl_datasets$$$function__1_store_numpy,
        mod_consts[15],
#if PYTHON_VERSION >= 0x300
        NULL,
#endif
        code_objects_68d7d53b79b82b605c7954c7e95042a6,
        NULL,
#if PYTHON_VERSION >= 0x300
        NULL,
        annotations,
#endif
        module_datasets,
        NULL,
        NULL,
        0
    );


    return (PyObject *)result;
}



static PyObject *MAKE_FUNCTION_datasets$$$function__2_rename_file(PyObject *annotations) {
    struct Nuitka_FunctionObject *result = Nuitka_Function_New(
        impl_datasets$$$function__2_rename_file,
        mod_consts[17],
#if PYTHON_VERSION >= 0x300
        NULL,
#endif
        code_objects_d309e91b5b42057bd4797ffea108dfcc,
        NULL,
#if PYTHON_VERSION >= 0x300
        NULL,
        annotations,
#endif
        module_datasets,
        NULL,
        NULL,
        0
    );


    return (PyObject *)result;
}


extern void _initCompiledCellType();
extern void _initCompiledGeneratorType();
extern void _initCompiledFunctionType();
extern void _initCompiledMethodType();
extern void _initCompiledFrameType();

extern PyTypeObject Nuitka_Loader_Type;

#ifdef _NUITKA_PLUGIN_DILL_ENABLED
// Provide a way to create find a function via its C code and create it back
// in another process, useful for multiprocessing extensions like dill
extern void registerDillPluginTables(PyThreadState *tstate, char const *module_name, PyMethodDef *reduce_compiled_function, PyMethodDef *create_compiled_function);

static function_impl_code const function_table_datasets[] = {
    impl_datasets$$$function__1_store_numpy,
    impl_datasets$$$function__2_rename_file,
    NULL
};

static PyObject *_reduce_compiled_function(PyObject *self, PyObject *args, PyObject *kwds) {
    PyObject *func;

    if (!PyArg_ParseTuple(args, "O:reduce_compiled_function", &func, NULL)) {
        return NULL;
    }

    PyThreadState *tstate = PyThreadState_GET();

    if (Nuitka_Function_Check(func) == false) {
        SET_CURRENT_EXCEPTION_TYPE0_STR(tstate, PyExc_TypeError, "not a compiled function");
        return NULL;
    }

    struct Nuitka_FunctionObject *function = (struct Nuitka_FunctionObject *)func;

    int offset = Nuitka_Function_GetFunctionCodeIndex(function, function_table_datasets);

    if (unlikely(offset == -1)) {
#if 0
        PRINT_STRING("Looking for:");
        PRINT_ITEM(func);
        PRINT_NEW_LINE();
#endif
        SET_CURRENT_EXCEPTION_TYPE0_STR(tstate, PyExc_TypeError, "Cannot find compiled function in module.");
        return NULL;
    }

    PyObject *code_object_desc = Nuitka_Function_ExtractCodeObjectDescription(tstate, function);

    PyObject *result = MAKE_TUPLE_EMPTY(tstate, 8);
    PyTuple_SET_ITEM(result, 0, Nuitka_PyLong_FromLong(offset));
    PyTuple_SET_ITEM(result, 1, code_object_desc);
    PyTuple_SET_ITEM0(result, 2, function->m_defaults);
#if PYTHON_VERSION >= 0x300
    PyTuple_SET_ITEM0(result, 3, function->m_kwdefaults ? function->m_kwdefaults : Py_None);
#else
    PyTuple_SET_ITEM_IMMORTAL(result, 3, Py_None);
#endif
    PyTuple_SET_ITEM0(result, 4, function->m_doc != NULL ? function->m_doc : Py_None);

    if (offset == -5) {
        CHECK_OBJECT(function->m_constant_return_value);
        PyTuple_SET_ITEM_IMMORTAL(result, 5, function->m_constant_return_value);
    } else {
        PyTuple_SET_ITEM_IMMORTAL(result, 5, Py_None);
    }

#if PYTHON_VERSION >= 0x300
    PyTuple_SET_ITEM0(result, 6, function->m_qualname);
#else
    PyTuple_SET_ITEM_IMMORTAL(result, 6, Py_None);
#endif

    PyObject *closure = PyObject_GetAttr(
        (PyObject *)function,
        const_str_plain___closure__
    );

    if (closure != Py_None) {
        for (Py_ssize_t i=0; i < PyTuple_GET_SIZE(closure); i++) {
            struct Nuitka_CellObject *cell = (struct Nuitka_CellObject *)PyTuple_GET_ITEM(closure, i);

            assert(Nuitka_Cell_Check((PyObject *)cell));

            PyTuple_SET_ITEM0(
                closure,
                i,
                cell->ob_ref
            );
        }
    }

    PyTuple_SET_ITEM(result, 7, closure);

    CHECK_OBJECT_DEEP(result);

    return result;
}

static PyMethodDef _method_def_reduce_compiled_function = {"reduce_compiled_function", (PyCFunction)_reduce_compiled_function,
                                                           METH_VARARGS, NULL};


static PyObject *_create_compiled_function(PyObject *self, PyObject *args, PyObject *kwds) {
    CHECK_OBJECT_DEEP(args);

    PyObject *function_index;
    PyObject *code_object_desc;
    PyObject *defaults;
    PyObject *kw_defaults;
    PyObject *doc;
    PyObject *constant_return_value;
    PyObject *function_qualname;
    PyObject *closure;

    if (!PyArg_ParseTuple(args, "OOOOOOOO:create_compiled_function", &function_index, &code_object_desc, &defaults, &kw_defaults, &doc, &constant_return_value, &function_qualname, &closure, NULL)) {
        return NULL;
    }

#if PYTHON_VERSION >= 0x300
    if (kw_defaults == Py_None) {
        kw_defaults = NULL;
    }
#endif

    return (PyObject *)Nuitka_Function_CreateFunctionViaCodeIndex(
        module_datasets,
        function_qualname,
        function_index,
        code_object_desc,
        constant_return_value,
        defaults,
        kw_defaults,
        doc,
        closure,
        function_table_datasets,
        sizeof(function_table_datasets) / sizeof(function_impl_code)
    );
}

static PyMethodDef _method_def_create_compiled_function = {
    "create_compiled_function",
    (PyCFunction)_create_compiled_function,
    METH_VARARGS, NULL
};


#endif

// Actual name might be different when loaded as a package.
#if defined(_NUITKA_MODULE) && 1
static char const *module_full_name = "datasets";
#endif

// Internal entry point for module code.
PyObject *modulecode_datasets(PyThreadState *tstate, PyObject *module, struct Nuitka_MetaPathBasedLoaderEntry const *loader_entry) {
    // Report entry to PGO.
    PGO_onModuleEntered("datasets");

    // Store the module for future use.
    module_datasets = module;

    moduledict_datasets = MODULE_DICT(module_datasets);

    // Modules can be loaded again in case of errors, avoid the init being done again.
    static bool init_done = false;

    if (init_done == false) {
#if defined(_NUITKA_MODULE) && 1
        // In case of an extension module loaded into a process, we need to call
        // initialization here because that's the first and potentially only time
        // we are going called.
#if PYTHON_VERSION > 0x350 && !defined(_NUITKA_EXPERIMENTAL_DISABLE_ALLOCATORS)
        initNuitkaAllocators();
#endif
        // Initialize the constant values used.
        _initBuiltinModule();

#if PYTHON_VERSION >= 0x3c0
        PyObject *real_module_name = PyObject_GetAttrString(module, "__name__");
        CHECK_OBJECT(real_module_name);
        module_full_name = strdup(Nuitka_String_AsString(real_module_name));
#endif

#if PYTHON_VERSION >= 0x3c0
        createGlobalConstants(tstate, real_module_name);
#else
        createGlobalConstants(tstate);
#endif
        /* Initialize the compiled types of Nuitka. */
        _initCompiledCellType();
        _initCompiledGeneratorType();
        _initCompiledFunctionType();
        _initCompiledMethodType();
        _initCompiledFrameType();

        _initSlotCompare();
#if PYTHON_VERSION >= 0x270
        _initSlotIterNext();
#endif

        patchTypeComparison();

        // Enable meta path based loader if not already done.
#ifdef _NUITKA_TRACE
        PRINT_STRING("datasets: Calling setupMetaPathBasedLoader().\n");
#endif
        setupMetaPathBasedLoader(tstate);
#if PYTHON_VERSION >= 0x3c0
        updateMetaPathBasedLoaderModuleRoot(module_full_name);
#endif


#if PYTHON_VERSION >= 0x300
        patchInspectModule(tstate);
#endif

#endif

        /* The constants only used by this module are created now. */
        NUITKA_PRINT_TRACE("datasets: Calling createModuleConstants().\n");
        createModuleConstants(tstate);

        createModuleCodeObjects();

        init_done = true;
    }

#if defined(_NUITKA_MODULE) && 1
    PyObject *pre_load = IMPORT_EMBEDDED_MODULE(tstate, "datasets" "-preLoad");
    if (pre_load == NULL) {
        return NULL;
    }
#endif

    // PRINT_STRING("in initdatasets\n");

#ifdef _NUITKA_PLUGIN_DILL_ENABLED
    {
        char const *module_name_c;
        if (loader_entry != NULL) {
            module_name_c = loader_entry->name;
        } else {
            PyObject *module_name = GET_STRING_DICT_VALUE(moduledict_datasets, (Nuitka_StringObject *)const_str_plain___name__);
            module_name_c = Nuitka_String_AsString(module_name);
        }

        registerDillPluginTables(tstate, module_name_c, &_method_def_reduce_compiled_function, &_method_def_create_compiled_function);
    }
#endif

    // Set "__compiled__" to what version information we have.
    UPDATE_STRING_DICT0(
        moduledict_datasets,
        (Nuitka_StringObject *)const_str_plain___compiled__,
        Nuitka_dunder_compiled_value
    );

    // Update "__package__" value to what it ought to be.
    {
#if 0
        UPDATE_STRING_DICT0(
            moduledict_datasets,
            (Nuitka_StringObject *)const_str_plain___package__,
            mod_consts[22]
        );
#elif 0
        PyObject *module_name = GET_STRING_DICT_VALUE(moduledict_datasets, (Nuitka_StringObject *)const_str_plain___name__);

        UPDATE_STRING_DICT0(
            moduledict_datasets,
            (Nuitka_StringObject *)const_str_plain___package__,
            module_name
        );
#else

#if PYTHON_VERSION < 0x300
        PyObject *module_name = GET_STRING_DICT_VALUE(moduledict_datasets, (Nuitka_StringObject *)const_str_plain___name__);
        char const *module_name_cstr = PyString_AS_STRING(module_name);

        char const *last_dot = strrchr(module_name_cstr, '.');

        if (last_dot != NULL) {
            UPDATE_STRING_DICT1(
                moduledict_datasets,
                (Nuitka_StringObject *)const_str_plain___package__,
                PyString_FromStringAndSize(module_name_cstr, last_dot - module_name_cstr)
            );
        }
#else
        PyObject *module_name = GET_STRING_DICT_VALUE(moduledict_datasets, (Nuitka_StringObject *)const_str_plain___name__);
        Py_ssize_t dot_index = PyUnicode_Find(module_name, const_str_dot, 0, PyUnicode_GetLength(module_name), -1);

        if (dot_index != -1) {
            UPDATE_STRING_DICT1(
                moduledict_datasets,
                (Nuitka_StringObject *)const_str_plain___package__,
                PyUnicode_Substring(module_name, 0, dot_index)
            );
        }
#endif
#endif
    }

    CHECK_OBJECT(module_datasets);

    // For deep importing of a module we need to have "__builtins__", so we set
    // it ourselves in the same way than CPython does. Note: This must be done
    // before the frame object is allocated, or else it may fail.

    if (GET_STRING_DICT_VALUE(moduledict_datasets, (Nuitka_StringObject *)const_str_plain___builtins__) == NULL) {
        PyObject *value = (PyObject *)builtin_module;

        // Check if main module, not a dict then but the module itself.
#if defined(_NUITKA_MODULE) || !0
        value = PyModule_GetDict(value);
#endif

        UPDATE_STRING_DICT0(moduledict_datasets, (Nuitka_StringObject *)const_str_plain___builtins__, value);
    }

    UPDATE_STRING_DICT0(moduledict_datasets, (Nuitka_StringObject *)const_str_plain___loader__, Nuitka_Loader_New(loader_entry));

#if PYTHON_VERSION >= 0x300
// Set the "__spec__" value

#if 0
    // Main modules just get "None" as spec.
    UPDATE_STRING_DICT0(moduledict_datasets, (Nuitka_StringObject *)const_str_plain___spec__, Py_None);
#else
    // Other modules get a "ModuleSpec" from the standard mechanism.
    {
        PyObject *bootstrap_module = getImportLibBootstrapModule();
        CHECK_OBJECT(bootstrap_module);

        PyObject *_spec_from_module = PyObject_GetAttrString(bootstrap_module, "_spec_from_module");
        CHECK_OBJECT(_spec_from_module);

        PyObject *spec_value = CALL_FUNCTION_WITH_SINGLE_ARG(tstate, _spec_from_module, module_datasets);
        Py_DECREF(_spec_from_module);

        // We can assume this to never fail, or else we are in trouble anyway.
        // CHECK_OBJECT(spec_value);

        if (spec_value == NULL) {
            PyErr_PrintEx(0);
            abort();
        }

// Mark the execution in the "__spec__" value.
        SET_ATTRIBUTE(tstate, spec_value, const_str_plain__initializing, Py_True);

        UPDATE_STRING_DICT1(moduledict_datasets, (Nuitka_StringObject *)const_str_plain___spec__, spec_value);
    }
#endif
#endif

    // Temp variables if any
    struct Nuitka_FrameObject *frame_57e560191028aae078dcbd68ca30bf96;
    NUITKA_MAY_BE_UNUSED char const *type_description_1 = NULL;
    bool tmp_result;
    struct Nuitka_ExceptionPreservationItem exception_state = Empty_Nuitka_ExceptionPreservationItem;
    NUITKA_MAY_BE_UNUSED int exception_lineno = 0;

    // Module init code if any


    // Module code.
    {
        PyObject *tmp_assign_source_1;
        tmp_assign_source_1 = Py_None;
        UPDATE_STRING_DICT0(moduledict_datasets, (Nuitka_StringObject *)mod_consts[5], tmp_assign_source_1);
    }
    {
        PyObject *tmp_assign_source_2;
        tmp_assign_source_2 = module_filename_obj;
        UPDATE_STRING_DICT0(moduledict_datasets, (Nuitka_StringObject *)mod_consts[6], tmp_assign_source_2);
    }
    frame_57e560191028aae078dcbd68ca30bf96 = MAKE_MODULE_FRAME(code_objects_57e560191028aae078dcbd68ca30bf96, module_datasets);

    // Push the new frame as the currently active one, and we should be exclusively
    // owning it.
    pushFrameStackCompiledFrame(tstate, frame_57e560191028aae078dcbd68ca30bf96);
    assert(Py_REFCNT(frame_57e560191028aae078dcbd68ca30bf96) == 2);

    // Framed code:
    {
        PyObject *tmp_assattr_value_1;
        PyObject *tmp_assattr_target_1;
        tmp_assattr_value_1 = module_filename_obj;
        tmp_assattr_target_1 = module_var_accessor_datasets_$$___spec__(tstate);
        assert(!(tmp_assattr_target_1 == NULL));
        tmp_result = SET_ATTRIBUTE(tstate, tmp_assattr_target_1, mod_consts[7], tmp_assattr_value_1);
        if (tmp_result == false) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 1;

            goto frame_exception_exit_1;
        }
    }
    {
        PyObject *tmp_assattr_value_2;
        PyObject *tmp_assattr_target_2;
        tmp_assattr_value_2 = Py_True;
        tmp_assattr_target_2 = module_var_accessor_datasets_$$___spec__(tstate);
        assert(!(tmp_assattr_target_2 == NULL));
        tmp_result = SET_ATTRIBUTE(tstate, tmp_assattr_target_2, mod_consts[8], tmp_assattr_value_2);
        if (tmp_result == false) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 1;

            goto frame_exception_exit_1;
        }
    }
    {
        PyObject *tmp_assign_source_3;
        tmp_assign_source_3 = Py_None;
        UPDATE_STRING_DICT0(moduledict_datasets, (Nuitka_StringObject *)mod_consts[9], tmp_assign_source_3);
    }
    {
        PyObject *tmp_assign_source_4;
        tmp_assign_source_4 = IMPORT_HARD_OS();
        assert(!(tmp_assign_source_4 == NULL));
        UPDATE_STRING_DICT0(moduledict_datasets, (Nuitka_StringObject *)mod_consts[10], tmp_assign_source_4);
    }
    {
        PyObject *tmp_assign_source_5;
        PyObject *tmp_name_value_1;
        PyObject *tmp_globals_arg_value_1;
        PyObject *tmp_locals_arg_value_1;
        PyObject *tmp_fromlist_value_1;
        PyObject *tmp_level_value_1;
        tmp_name_value_1 = mod_consts[11];
        tmp_globals_arg_value_1 = (PyObject *)moduledict_datasets;
        tmp_locals_arg_value_1 = Py_None;
        tmp_fromlist_value_1 = Py_None;
        tmp_level_value_1 = const_int_0;
        frame_57e560191028aae078dcbd68ca30bf96->m_frame.f_lineno = 2;
        tmp_assign_source_5 = IMPORT_MODULE5(tstate, tmp_name_value_1, tmp_globals_arg_value_1, tmp_locals_arg_value_1, tmp_fromlist_value_1, tmp_level_value_1);
        if (tmp_assign_source_5 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 2;

            goto frame_exception_exit_1;
        }
        UPDATE_STRING_DICT1(moduledict_datasets, (Nuitka_StringObject *)mod_consts[2], tmp_assign_source_5);
    }
    {
        PyObject *tmp_assign_source_6;
        PyObject *tmp_path_arg_1;
        tmp_path_arg_1 = module_var_accessor_datasets_$$___file__(tstate);
        if (unlikely(tmp_path_arg_1 == NULL)) {
            RAISE_CURRENT_EXCEPTION_NAME_ERROR(tstate, &exception_state, mod_consts[6]);
        }

        if (tmp_path_arg_1 == NULL) {
            assert(HAS_EXCEPTION_STATE(&exception_state));



            exception_lineno = 4;

            goto frame_exception_exit_1;
        }
        tmp_assign_source_6 = OS_PATH_DIRNAME(tstate, tmp_path_arg_1);
        if (tmp_assign_source_6 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 4;

            goto frame_exception_exit_1;
        }
        UPDATE_STRING_DICT1(moduledict_datasets, (Nuitka_StringObject *)mod_consts[12], tmp_assign_source_6);
    }
    {
        PyObject *tmp_assign_source_7;
        PyObject *tmp_called_value_1;
        PyObject *tmp_expression_value_1;
        PyObject *tmp_args_element_value_1;
        PyObject *tmp_args_element_value_2;
        tmp_expression_value_1 = IMPORT_HARD_POSIXPATH();
        assert(!(tmp_expression_value_1 == NULL));
        tmp_called_value_1 = LOOKUP_ATTRIBUTE(tstate, tmp_expression_value_1, mod_consts[0]);
        if (tmp_called_value_1 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 5;

            goto frame_exception_exit_1;
        }
        tmp_args_element_value_1 = module_var_accessor_datasets_$$_dirname(tstate);
        assert(!(tmp_args_element_value_1 == NULL));
        tmp_args_element_value_2 = mod_consts[13];
        frame_57e560191028aae078dcbd68ca30bf96->m_frame.f_lineno = 5;
        {
            PyObject *call_args[] = {tmp_args_element_value_1, tmp_args_element_value_2};
            tmp_assign_source_7 = CALL_FUNCTION_WITH_ARGS2(tstate, tmp_called_value_1, call_args);
        }

        Py_DECREF(tmp_called_value_1);
        if (tmp_assign_source_7 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 5;

            goto frame_exception_exit_1;
        }
        UPDATE_STRING_DICT1(moduledict_datasets, (Nuitka_StringObject *)mod_consts[1], tmp_assign_source_7);
    }


    // Put the previous frame back on top.
    popFrameStack(tstate);

    goto frame_no_exception_1;
    frame_exception_exit_1:


    {
        PyTracebackObject *exception_tb = GET_EXCEPTION_STATE_TRACEBACK(&exception_state);
        if (exception_tb == NULL) {
            exception_tb = MAKE_TRACEBACK(frame_57e560191028aae078dcbd68ca30bf96, exception_lineno);
            SET_EXCEPTION_STATE_TRACEBACK(&exception_state, exception_tb);
        } else if (exception_tb->tb_frame != &frame_57e560191028aae078dcbd68ca30bf96->m_frame) {
            exception_tb = ADD_TRACEBACK(exception_tb, frame_57e560191028aae078dcbd68ca30bf96, exception_lineno);
            SET_EXCEPTION_STATE_TRACEBACK(&exception_state, exception_tb);
        }
    }



    assertFrameObject(frame_57e560191028aae078dcbd68ca30bf96);

    // Put the previous frame back on top.
    popFrameStack(tstate);

    // Return the error.
    goto module_exception_exit;
    frame_no_exception_1:;
    {
        PyObject *tmp_assign_source_8;
        PyObject *tmp_annotations_1;
        tmp_annotations_1 = DICT_COPY(tstate, mod_consts[14]);


        tmp_assign_source_8 = MAKE_FUNCTION_datasets$$$function__1_store_numpy(tmp_annotations_1);

        UPDATE_STRING_DICT1(moduledict_datasets, (Nuitka_StringObject *)mod_consts[15], tmp_assign_source_8);
    }
    {
        PyObject *tmp_assign_source_9;
        PyObject *tmp_annotations_2;
        tmp_annotations_2 = DICT_COPY(tstate, mod_consts[16]);


        tmp_assign_source_9 = MAKE_FUNCTION_datasets$$$function__2_rename_file(tmp_annotations_2);

        UPDATE_STRING_DICT1(moduledict_datasets, (Nuitka_StringObject *)mod_consts[17], tmp_assign_source_9);
    }

    // Report to PGO about leaving the module without error.
    PGO_onModuleExit("datasets", false);

#if defined(_NUITKA_MODULE) && 1
    {
        PyObject *post_load = IMPORT_EMBEDDED_MODULE(tstate, "datasets" "-postLoad");
        if (post_load == NULL) {
            return NULL;
        }
    }
#endif

    Py_INCREF(module_datasets);
    return module_datasets;
    module_exception_exit:

#if defined(_NUITKA_MODULE) && 1
    {
        PyObject *module_name = GET_STRING_DICT_VALUE(moduledict_datasets, (Nuitka_StringObject *)const_str_plain___name__);

        if (module_name != NULL) {
            Nuitka_DelModule(tstate, module_name);
        }
    }
#endif
    PGO_onModuleExit("datasets", false);

    RESTORE_ERROR_OCCURRED_STATE(tstate, &exception_state);
    return NULL;
}


/* Visibility definitions to make the DLL entry point exported */
#if defined(__GNUC__)

#if PYTHON_VERSION < 0x300

#if defined(_WIN32)
#define NUITKA_MODULE_INIT_FUNCTION __declspec(dllexport) PyMODINIT_FUNC
#else
#define NUITKA_MODULE_INIT_FUNCTION PyMODINIT_FUNC __attribute__((visibility("default")))
#endif

#else

#if defined(_WIN32)
#define NUITKA_MODULE_INIT_FUNCTION __declspec(dllexport) PyObject *
#else

#ifdef __cplusplus
#define NUITKA_MODULE_INIT_FUNCTION extern "C" __attribute__((visibility("default"))) PyObject *
#else
#define NUITKA_MODULE_INIT_FUNCTION __attribute__((visibility("default"))) PyObject *
#endif

#endif
#endif

#else
#define NUITKA_MODULE_INIT_FUNCTION PyMODINIT_FUNC
#endif

static PyObject *orig_dunder_file_value;

#if PYTHON_VERSION >= 0x300
static setattrofunc orig_PyModule_Type_tp_setattro;

/* This is used one time only. */
static int Nuitka_TopLevelModule_tp_setattro(PyObject *module, PyObject *name, PyObject *value) {
    PyModule_Type.tp_setattro = orig_PyModule_Type_tp_setattro;

    if (orig_dunder_file_value != NULL) {
        UPDATE_STRING_DICT0(
            moduledict_datasets,
            (Nuitka_StringObject *)const_str_plain___file__,
            orig_dunder_file_value
        );
    }

    // Prevent "__spec__" update as well.
#if PYTHON_VERSION >= 0x300
    if (PyUnicode_Check(name) && PyUnicode_Compare(name, const_str_plain___spec__) == 0) {
        return 0;
    }
#endif

    return orig_PyModule_Type_tp_setattro(module, name, value);
}
#endif

#if PYTHON_VERSION >= 0x300
static struct PyModuleDef mdef_datasets = {
    PyModuleDef_HEAD_INIT,
    NULL,                /* m_name, filled later */
    NULL,                /* m_doc */
    -1, /* m_size */
    NULL,                /* m_methods */
    NULL,                /* m_slots */
    NULL,                /* m_traverse */
    NULL,                /* m_clear */
    NULL,                /* m_free */
};
#endif

#if PYTHON_VERSION < 0x300
static void onModuleFileValueRelease(void *v) {
    if (orig_dunder_file_value != NULL) {
        UPDATE_STRING_DICT0(
            moduledict_datasets,
            (Nuitka_StringObject *)const_str_plain___file__,
            orig_dunder_file_value
        );
    }
}
#endif

/* The exported interface to CPython. On import of the module, this function
 * gets called. It has to have an exact function name, in cases it's a shared
 * library export.
 */


static PyObject *PyInit_datasets_phase2(PyObject *module) {
    PyThreadState *tstate = PyThreadState_GET();

    PyObject *result = modulecode_datasets(tstate, module, NULL);

#if PYTHON_VERSION < 0x300
    // Our "__file__" value will not be respected by CPython and one
    // way we can avoid it, is by having a capsule type, that when
    // it gets released, we are called and repair the value.

    if (HAS_ERROR_OCCURRED(tstate) == false) {
        orig_dunder_file_value = DICT_GET_ITEM_WITH_HASH_ERROR1(tstate, (PyObject *)moduledict_datasets, const_str_plain___file__);

        PyObject *fake_file_value = PyCObject_FromVoidPtr(NULL, onModuleFileValueRelease);

        UPDATE_STRING_DICT1(
            moduledict_datasets,
            (Nuitka_StringObject *)const_str_plain___file__,
            fake_file_value
        );
    }
#else
    if (result != NULL) {
        // Make sure we undo the change of the "__file__" attribute during importing. We do not
        // know how to achieve it for Python2 though. TODO: Find something for Python2 too.
        orig_PyModule_Type_tp_setattro = PyModule_Type.tp_setattro;
        PyModule_Type.tp_setattro = Nuitka_TopLevelModule_tp_setattro;

        orig_dunder_file_value = DICT_GET_ITEM_WITH_HASH_ERROR1(tstate, (PyObject *)moduledict_datasets, const_str_plain___file__);
    }
#endif

    return result;
}

#if -1 >= 0
static int PyInit_datasets_slot(PyObject *module) {
    PyObject *result = PyInit_datasets_phase2(module);

    if (result == NULL) {
        return 1;
    } else {
        return 0;
    }
}
#endif

NUITKA_MODULE_INIT_FUNCTION (PyInit_datasets)(void) {
#if PYTHON_VERSION < 0x3c0
    if (_Py_PackageContext != NULL) {
        if (strcmp(module_full_name, _Py_PackageContext) != 0) {
            module_full_name = strdup(_Py_PackageContext);
        }
    }
#endif

#if PYTHON_VERSION < 0x300
    PyObject *module = Py_InitModule4(
        module_full_name,        // Module Name
        NULL,                    // No methods initially, all are added
                                 // dynamically in actual module code only.
        NULL,                    // No "__doc__" is initially set, as it could
                                 // not contain NUL this way, added early in
                                 // actual code.
        NULL,                    // No self for modules, we don't use it.
        PYTHON_API_VERSION
    );
#else
    mdef_datasets.m_name = module_full_name;

#if -1 == -1
    PyObject *module = PyModule_Create(&mdef_datasets);
    CHECK_OBJECT(module);

    {
        NUITKA_MAY_BE_UNUSED bool res = Nuitka_SetModuleString(module_full_name, module);
        assert(res != false);
    }

#endif
#endif

#if -1 >= 0
    static PyModuleDef_Slot _module_slots[] = {
        {Py_mod_exec, PyInit_datasets_slot},
        {0, NULL}
    };

    mdef_datasets.m_slots = _module_slots;

    return PyModuleDef_Init(&mdef_datasets);
#elif PYTHON_VERSION >= 0x300
    return PyInit_datasets_phase2(module);
#else
    PyInit_datasets_phase2(module);
#endif
}
