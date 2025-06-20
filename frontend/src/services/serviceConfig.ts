import axios, { AxiosRequestConfig } from "axios";
// import Services from "./serviceUrls";

interface TErrorResponse {
  detail: string;
  [key: string]: string | string[] | number | boolean | undefined;
}

interface TApiSuccess<T> {
  success: true;
  data: T;
}

interface TApiFailure {
  success: false;
  status: number;
  error: TErrorResponse;
}

type TApiResponse<T> = TApiSuccess<T> | TApiFailure;

const instance = axios.create({
  baseURL: process.env.NEXT_PUBLIC_SERVER_API_URL as string,
  timeout: 300000,
  headers: {
    Accept: "application/json",
    "content-type": "application/json",
  },
});

const formDataInstance = axios.create({
  baseURL: process.env.NEXT_PUBLIC_SERVER_API_URL as string,
  timeout: 100000,
  headers: {
    Accept: "application/json",
    "content-type": "multipart/form-data",
  },
});

// async function handleTokenRefresh<TResponse>(
//   originalRequest: AxiosRequestConfig,
// ): Promise<TApiResponse<TResponse>> {
//   // retry the original request
//   return await axios<TResponse>(originalRequest)
//     .then(
//       (retryResponse) =>
//         // return the retired request data
//         ({
//           success: true,
//           data: retryResponse.data,
//         }) as TApiResponse<TResponse>,
//     )
//     .catch((retryError) => {
//       console.error("Retry failed: ", retryError);
//       return {
//         success: false,
//         status: retryError.status,
//         error: { detail: "Retry failed!", error: retryError },
//       };
//     });
// }
//
// async function handle401Error<TResponse>(
//   originalRequest: AxiosRequestConfig,
// ): Promise<TApiResponse<TResponse>> {
//   try {
//     // try to refresh token
//     await instance.post<TResponse>(
//       Services.refresh,
//       {},
//       { withCredentials: true },
//     );
//
//     // if refreshed successfully
//     return await handleTokenRefresh(originalRequest);
//   } catch (error) {
//     // the tokens are now expired
//     console.error("Refresh token error: ", error);
//     // ------------------------------------------
//     // delete tokens from user and logout the user
//     //
//     // handler block when the tokens expire
//     // ------------------------------------------
//     return {
//       success: false,
//       status: 401,
//       error: {
//         detail: "Refresh token expired!",
//         error: error,
//       } as TErrorResponse,
//     };
//   }
// }

async function requestFailureCallback<TResponse>(
  error: unknown,
): Promise<TApiResponse<TResponse>> {
  if (!axios.isAxiosError(error)) {
    // error is unknown and unexpected
    console.error("Error: ", error);
    return {
      success: false,
      status: 0,
      error: { detail: "An unexpected error occurred!" } as TErrorResponse,
    };
  }

  if (error.code === "ERR_NETWORK") {
    return {
      success: false,
      status: 0,
      error: { detail: "Network error!" },
    };
  }

  if (!error.response) {
    return {
      success: false,
      status: 0,
      error: { detail: "Unknown network error occured!" },
    };
  }

  const originalRequest = error.config as AxiosRequestConfig;

  if (!originalRequest) {
    console.error("Original request config not found!");
    return {
      success: false,
      status: error.response.status,
      error: { detail: "An unexpected error occurred!" },
    };
  }

  // if (error.response.status === 401) {
  //   return await handle401Error<TResponse>(originalRequest);
  // }

  // other error by server
  return {
    success: false,
    status: error.response.status,
    error: {
      detail: "Request failed with status: " + error.response.status,
      data: error.response.data,
    },
  };
}

async function get<TRequest, TResponse>(
  url: string,
  options?: { params?: TRequest; withCredentials?: boolean },
): Promise<TApiResponse<TResponse>> {
  try {
    const response = await instance.get<TResponse>(url, {
      params: options?.params ?? {},
      withCredentials: options?.withCredentials ?? false,
    });
    return { success: true, data: response.data };
  } catch (error) {
    return requestFailureCallback(error);
  }
}

async function put<TRequest, TRequestParams, TResponse>(
  url: string,
  data: TRequest,
  options?: {
    params?: TRequestParams;
    withCredentials?: boolean;
  },
): Promise<TApiResponse<TResponse>> {
  try {
    const response = await instance.put<TResponse>(url, data, {
      params: options?.params ?? {},
      withCredentials: options?.withCredentials ?? false,
    });
    return { success: true, data: response.data };
  } catch (error) {
    return requestFailureCallback(error);
  }
}

async function patch<TRequest, TRequestParams, TResponse>(
  url: string,
  data: TRequest,
  options?: {
    params?: TRequestParams;
    withCredentials?: boolean;
  },
): Promise<TApiResponse<TResponse>> {
  try {
    const response = await instance.patch<TResponse>(url, data, {
      params: options?.params ?? {},
      withCredentials: options?.withCredentials ?? false,
    });
    return { success: true, data: response.data };
  } catch (error) {
    return requestFailureCallback(error);
  }
}

async function post<TRequest, TRequestParams, TResponse>(
  url: string,
  data: TRequest,
  options?: {
    params?: TRequestParams;
    withCredentials?: boolean;
  },
): Promise<TApiResponse<TResponse>> {
  try {
    const response = await instance.post<TResponse>(url, data, {
      params: options?.params ?? {},
      withCredentials: options?.withCredentials ?? false,
    });
    return { success: true, data: response.data };
  } catch (error) {
    return requestFailureCallback(error);
  }
}

async function delete_<TRequest, TResponse>(
  url: string,
  options?: { params?: TRequest; withCredentials?: boolean },
): Promise<TApiResponse<TResponse>> {
  try {
    const response = await instance.delete<TResponse>(url, {
      params: options?.params ?? {},
      withCredentials: options?.withCredentials ?? false,
    });
    return { success: true, data: response.data };
  } catch (error) {
    return requestFailureCallback(error);
  }
}

async function formData_put<TRequest, TRequestParams, TResponse>(
  url: string,
  data: TRequest,
  options?: {
    params?: TRequestParams;
    withCredentials?: boolean;
  },
): Promise<TApiResponse<TResponse>> {
  try {
    const response = await formDataInstance.put<TResponse>(url, data, {
      params: options?.params ?? {},
      withCredentials: options?.withCredentials ?? false,
    });
    return { success: true, data: response.data };
  } catch (error) {
    return requestFailureCallback(error);
  }
}

async function formData_patch<TRequest, TRequestParams, TResponse>(
  url: string,
  data: TRequest,
  options?: {
    params?: TRequestParams;
    withCredentials?: boolean;
  },
): Promise<TApiResponse<TResponse>> {
  try {
    const response = await formDataInstance.patch<TResponse>(url, data, {
      params: options?.params ?? {},
      withCredentials: options?.withCredentials ?? false,
    });
    return { success: true, data: response.data };
  } catch (error) {
    return requestFailureCallback(error);
  }
}

async function formData_post<TRequest, TRequestParams, TResponse>(
  url: string,
  data: TRequest,
  options?: {
    params?: TRequestParams;
    withCredentials?: boolean;
  },
): Promise<TApiResponse<TResponse>> {
  try {
    const response = await formDataInstance.post<TResponse>(url, data, {
      params: options?.params ?? {},
      withCredentials: options?.withCredentials ?? false,
    });
    return { success: true, data: response.data };
  } catch (error) {
    return requestFailureCallback(error);
  }
}

export {
  get,
  put,
  patch,
  post,
  delete_,
  formData_put,
  formData_patch,
  formData_post,
};

export type { TApiResponse, TErrorResponse };
