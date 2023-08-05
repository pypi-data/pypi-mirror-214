/**
 * FastAPI
 * No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)
 *
 * The version of the OpenAPI document: 0.1.0
 *
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */
import * as runtime from '../runtime';
import type { Plugin } from '../models';
export interface GetEntrypointRequest {
    name: string;
}
/**
 *
 */
export declare class PluginsApi extends runtime.BaseAPI {
    /**
     * Get the frontend entrypoint for a plugin
     *
     */
    getEntrypointRaw(requestParameters: GetEntrypointRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<any>>;
    /**
     * Get the frontend entrypoint for a plugin
     *
     */
    getEntrypoint(requestParameters: GetEntrypointRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<any>;
    /**
     * Get a list of all the installed spotlight plugins
     *
     */
    getPluginsRaw(initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<Array<Plugin>>>;
    /**
     * Get a list of all the installed spotlight plugins
     *
     */
    getPlugins(initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<Array<Plugin>>;
}
