//
// Copyright 2016 The BigDL Authors.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//

#pragma once

#include <string>
#include <vector>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdbool.h>
#include <memory>
#include <vector>

#include "common.h"

using namespace std;

#ifdef __linux__
#define EXPORT_API extern "C"
#else
#define EXPORT_API extern "C" __declspec(dllexport)
#endif


class NPUModel;

#ifdef __cplusplus
extern "C" {
#endif
    EXPORT_API void load_tokenizer(tokenizer_params &tok_params, std::string model_str);

    EXPORT_API vector<int32_t> llm_tokenize(std::string prompt, bool add_special);

    EXPORT_API std::string llm_decode(vector<int32_t> tokens);

    EXPORT_API extern NPUModel* load_model_from_file(npu_model_params &model_params, std::string model_str);

    EXPORT_API std::string add_chat_template(npu_model_params model_params, std::string input_prompt);

    EXPORT_API float* run_prefill(NPUModel* model, std::vector<int32_t> embd_inp);

    EXPORT_API float* run_decode(NPUModel* model, int32_t input_token);

    EXPORT_API int32_t llm_sample_token(float* logits, bool greedy_search, npu_model_params model_params);

    EXPORT_API void reset(NPUModel* model);

#ifdef __cplusplus
}
#endif
