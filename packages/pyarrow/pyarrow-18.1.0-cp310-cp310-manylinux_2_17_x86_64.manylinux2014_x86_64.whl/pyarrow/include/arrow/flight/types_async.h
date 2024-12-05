// Licensed to the Apache Software Foundation (ASF) under one
// or more contributor license agreements.  See the NOTICE file
// distributed with this work for additional information
// regarding copyright ownership.  The ASF licenses this file
// to you under the Apache License, Version 2.0 (the
// "License"); you may not use this file except in compliance
// with the License.  You may obtain a copy of the License at
//
//   http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing,
// software distributed under the License is distributed on an
// "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
// KIND, either express or implied.  See the License for the
// specific language governing permissions and limitations
// under the License.

#pragma once

#include <memory>

#include "arrow/flight/type_fwd.h"
#include "arrow/flight/types.h"
#include "arrow/ipc/options.h"
#include "arrow/type_fwd.h"

namespace arrow::flight {

/// \defgroup flight-async Async Flight Types
/// Common types used for asynchronous Flight APIs.
/// @{

/// \brief Non-templated state for an async RPC.
class ARROW_FLIGHT_EXPORT AsyncListenerBase {
 public:
  AsyncListenerBase();
  virtual ~AsyncListenerBase();

  /// \brief Request cancellation of the RPC.
  ///
  /// The RPC is not cancelled until AsyncListener::OnFinish is called.
  void TryCancel();

 private:
  friend class arrow::flight::internal::ClientTransport;

  /// Transport-specific state for this RPC.  Transport
  /// implementations may store and retrieve state here via
  /// ClientTransport::SetAsyncRpc and ClientTransport::GetAsyncRpc.
  std::unique_ptr<internal::AsyncRpc> rpc_state_;
};

/// \brief Callbacks for results from async RPCs.
///
/// A single listener may not be used for multiple concurrent RPC
/// calls.  The application MUST hold the listener alive until
/// OnFinish() is called and has finished.
template <typename T>
class ARROW_FLIGHT_EXPORT AsyncListener : public AsyncListenerBase {
 public:
  /// \brief Get the next server result.
  ///
  /// This will never be called concurrently with itself or OnFinish.
  virtual void OnNext(T message) = 0;
  /// \brief Get the final status.
  ///
  /// This will never be called concurrently with itself or OnNext.  If the
  /// error comes from the remote server, then a TransportStatusDetail will be
  /// attached.  Otherwise, the error is generated by the client-side
  /// transport and will not have a TransportStatusDetail.
  virtual void OnFinish(Status status) = 0;
};

/// @}

}  // namespace arrow::flight
