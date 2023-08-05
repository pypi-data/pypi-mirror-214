import { HTMLManager } from "@jupyter-widgets/html-manager";
import { WidgetModel, WidgetView, IModelOptions, IClassicComm } from "@jupyter-widgets/base";
import { IManagerState } from "@jupyter-widgets/base-manager";
export type ModelBundle = {
    spec: {
        model_id: string;
    };
    state: IManagerState;
};
export declare class WidgetManager extends HTMLManager {
    private _known_models;
    private kernel_manager;
    private kernel;
    private ws;
    private _model_objs;
    bk_send?: (data: string | ArrayBuffer) => void;
    bk_open(send_fn: (data: string | ArrayBuffer) => void): void;
    bk_recv(data: string | ArrayBuffer): void;
    private _comms;
    constructor(options: any);
    _attach_comm(comm: any, model: WidgetModel): void;
    render(bundle: ModelBundle, el: HTMLElement): Promise<WidgetView | null>;
    _create_comm(target_name: string, model_id: string, data?: any, metadata?: any, buffers?: ArrayBuffer[] | ArrayBufferView[]): Promise<IClassicComm>;
    _get_comm_info(): Promise<{}>;
    new_model(options: IModelOptions, serialized_state?: any): Promise<WidgetModel>;
    protected loadClass(className: string, moduleName: string, moduleVersion: string): Promise<typeof WidgetModel | typeof WidgetView>;
}
//# sourceMappingURL=manager.d.ts.map