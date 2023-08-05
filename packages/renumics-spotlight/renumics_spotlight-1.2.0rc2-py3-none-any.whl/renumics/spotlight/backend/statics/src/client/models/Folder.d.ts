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
import type { FileEntry } from './FileEntry';
/**
 * A single folder
 * @export
 * @interface Folder
 */
export interface Folder {
    /**
     *
     * @type {string}
     * @memberof Folder
     */
    name: string;
    /**
     *
     * @type {string}
     * @memberof Folder
     */
    path: string;
    /**
     *
     * @type {string}
     * @memberof Folder
     */
    parent?: string;
    /**
     *
     * @type {Array<FileEntry>}
     * @memberof Folder
     */
    files: Array<FileEntry>;
}
/**
 * Check if a given object implements the Folder interface.
 */
export declare function instanceOfFolder(value: object): boolean;
export declare function FolderFromJSON(json: any): Folder;
export declare function FolderFromJSONTyped(json: any, ignoreDiscriminator: boolean): Folder;
export declare function FolderToJSON(value?: Folder | null): any;
