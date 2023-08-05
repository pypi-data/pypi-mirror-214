import * as base from "@jupyter-widgets/base";
import * as outputWidgets from "@jupyter-widgets/output";
import * as controls from "@jupyter-widgets/controls";
import { HTMLManager } from "@jupyter-widgets/html-manager";
import { shims } from "@jupyter-widgets/base";
import { KernelManager } from "@jupyterlab/services";
import { isString } from "@bokehjs/core/util/types";
import { keys, entries, to_object } from "@bokehjs/core/util/object";
class CommsWebSocket {
    constructor(url, _protocols) {
        this.CONNECTING = 0;
        this.OPEN = 1;
        this.CLOSING = 2;
        this.CLOSED = 3;
        this.onclose = null;
        this.onerror = null;
        this.onmessage = null;
        this.onopen = null;
        this.url = url instanceof URL ? url.toString() : url;
    }
    close(code, reason) {
        var _a;
        const event = new CloseEvent("close", { code, reason });
        (_a = this.onclose) === null || _a === void 0 ? void 0 : _a.call(this, event);
    }
    addEventListener(_type, _listener, _options) {
        throw new Error("not implemented");
    }
    removeEventListener(_type, _listener, _options) {
        throw new Error("not implemented");
    }
    dispatchEvent(_event) {
        throw new Error("not implemented");
    }
}
CommsWebSocket.CONNECTING = 0;
CommsWebSocket.OPEN = 1;
CommsWebSocket.CLOSING = 2;
CommsWebSocket.CLOSED = 3;
let _kernel_id = 0;
export class WidgetManager extends HTMLManager {
    bk_open(send_fn) {
        var _a, _b;
        if (this.ws != null) {
            this.bk_send = send_fn;
            (_b = (_a = this.ws).onopen) === null || _b === void 0 ? void 0 : _b.call(_a, new Event("open"));
        }
    }
    bk_recv(data) {
        var _a, _b;
        if (this.ws != null) {
            (_b = (_a = this.ws).onmessage) === null || _b === void 0 ? void 0 : _b.call(_a, new MessageEvent("message", { data }));
        }
    }
    constructor(options) {
        super(options);
        this._known_models = new Map();
        this.ws = null;
        this._model_objs = new Map();
        this._comms = new Map();
        const manager = this;
        const settings = {
            appendToken: false,
            baseUrl: "",
            appUrl: "",
            wsUrl: "",
            token: "",
            init: { cache: "no-store", credentials: "same-origin" },
            fetch: async (_input, _init) => {
                // returns an empty list of kernels to make KernelManager happy
                return new Response("[]", { status: 200 });
            },
            Headers,
            Request,
            WebSocket: class extends CommsWebSocket {
                constructor(url, protocols) {
                    super(url, protocols);
                    manager.ws = this;
                }
                send(data) {
                    var _a;
                    if (isString(data) || data instanceof ArrayBuffer) {
                        (_a = manager.bk_send) === null || _a === void 0 ? void 0 : _a.call(manager, data);
                    }
                    else {
                        console.error(`only string and ArrayBuffer types are supported, got ${typeof data}`);
                    }
                }
            },
        };
        this.kernel_manager = new KernelManager({ serverSettings: settings });
        const kernel_model = { name: "bokeh_kernel", id: `${_kernel_id++}` };
        this.kernel = this.kernel_manager.connectTo({ model: kernel_model, handleComms: true });
        this.kernel.registerCommTarget(this.comm_target_name, (comm, msg) => {
            const model = this._model_objs.get(msg.content.comm_id);
            const comm_wrapper = new shims.services.Comm(comm);
            if (model == null) {
                this.handle_comm_open(comm_wrapper, msg).then((model) => {
                    if (model != null && !model.comm_live) {
                        const comm_wrapper = new shims.services.Comm(comm);
                        this._attach_comm(comm_wrapper, model);
                    }
                });
            }
            if (model != null && !model.comm_live) {
                this._attach_comm(comm_wrapper, model);
            }
            this._model_objs.delete(msg.content.comm_id);
        });
    }
    _attach_comm(comm, model) {
        model.comm = comm;
        // Hook comm messages up to model.
        comm.on_close(model._handle_comm_closed.bind(model));
        comm.on_msg(model._handle_comm_msg.bind(model));
        model.comm_live = true;
    }
    async render(bundle, el) {
        const { spec, state } = bundle;
        const new_models = state.state;
        for (const [id, new_model] of entries(new_models)) {
            this._known_models.set(id, new_model);
        }
        try {
            const models = await this.set_state(state);
            await this.set_state(Object.assign(Object.assign({}, state), { state: state.full_state }));
            for (const model of models) {
                if (this._model_objs.has(model.model_id))
                    continue;
                const comm = await this._create_comm(this.comm_target_name, model.model_id);
                this._attach_comm(comm, model);
                this._model_objs.set(model.model_id, model);
                model.once("comm:close", () => {
                    this._model_objs.delete(model.model_id);
                });
            }
            const model = models.find((item) => item.model_id == spec.model_id);
            if (model == null) {
                return null;
            }
            const view = await this.create_view(model, { el });
            await this.display_view(view, el);
            return view;
        }
        finally {
            for (const id of keys(new_models)) {
                this._known_models.delete(id);
            }
        }
    }
    async _create_comm(target_name, model_id, data, metadata, buffers) {
        const comm = (() => {
            const key = target_name + model_id;
            const comm = this._comms.get(key);
            if (comm != null)
                return comm;
            else {
                const comm = this.kernel.createComm(target_name, model_id);
                this._comms.set(key, comm);
                return comm;
            }
        })();
        comm.open(data, metadata, buffers);
        return new shims.services.Comm(comm);
    }
    _get_comm_info() {
        return Promise.resolve(to_object(this._known_models));
    }
    async new_model(options, serialized_state) {
        // XXX: this is a hack that allows to connect to a live comm and use initial
        // state sent via a state bundle, essentially turning new_model(modelCreate)
        // into new_model(modelCreate, modelState) in ManagerBase.set_state(), possibly
        // breaking safe guard rule (1) of that method. This is done this way to avoid
        // reimplementing set_state().
        if (serialized_state === undefined) {
            const models = this._known_models;
            const { model_id } = options;
            if (model_id != null && models.has(model_id)) {
                const model = models.get(model_id);
                serialized_state = model.state;
            }
            else
                throw new Error("internal error in new_model()");
        }
        return super.new_model(options, serialized_state);
    }
    loadClass(className, moduleName, moduleVersion) {
        return new Promise((resolve, reject) => {
            if (moduleName === "@jupyter-widgets/base") {
                resolve(base);
            }
            else if (moduleName === "@jupyter-widgets/controls") {
                resolve(controls);
            }
            else if (moduleName === "@jupyter-widgets/output") {
                resolve(outputWidgets);
            }
            else if (this.loader !== undefined) {
                resolve(this.loader(moduleName, moduleVersion));
            }
            else {
                reject(`Could not load module ${moduleName}@${moduleVersion}`);
            }
        }).then((module) => {
            if (module[className]) {
                return module[className];
            }
            else {
                return Promise.reject(`Class ${className} not found in module ${moduleName}@${moduleVersion}`);
            }
        });
    }
}
