var _a;
import { div, InlineStyleSheet } from "@bokehjs/core/dom";
import { LayoutDOM, LayoutDOMView } from "@bokehjs/models/layouts/layout_dom";
import { MessageSentEvent } from "@bokehjs/document/events";
import { isString } from "@bokehjs/core/util/types";
import { assert } from "@bokehjs/core/util/assert";
import { generate_require_loader } from "./loader";
import { WidgetManager } from "./manager";
const widget_managers = new WeakMap();
export class IPyWidgetView extends LayoutDOMView {
    constructor() {
        super(...arguments);
        this.rendered = false;
        this.ipy_view = null;
    }
    get child_models() {
        return [];
    }
    connect_signals() {
        super.connect_signals();
        const observer = new MutationObserver((mutations) => {
            for (const mutation of mutations) {
                for (const node of [...mutation.addedNodes, ...mutation.removedNodes]) {
                    if (node instanceof HTMLStyleElement) {
                        this._update_stylesheets();
                        break;
                    }
                }
            }
        });
        observer.observe(document.head, { childList: true });
    }
    _ipy_stylesheets() {
        const stylesheets = [];
        for (const child of document.head.children) {
            if (child instanceof HTMLStyleElement) {
                const raw_css = child.textContent;
                if (raw_css != null) {
                    const css = raw_css.replace(/:root/g, ":host");
                    stylesheets.push(new InlineStyleSheet(css));
                }
            }
        }
        return stylesheets;
    }
    stylesheets() {
        return [...super.stylesheets(), ...this._ipy_stylesheets()];
    }
    render() {
        super.render();
        this.container = div({ style: "display: contents;" }); // ipywidgets' APIs require HTMLElement, not DocumentFragment
        this.shadow_el.append(this.container);
        this._render().then(() => {
            this.invalidate_layout(); // TODO: this may be overzealous; probably should be removed
            this.rendered = true;
            this.notify_finished();
        });
    }
    has_finished() {
        return this.rendered && super.has_finished();
    }
    async _render() {
        if (this.ipy_view == null) {
            const { document } = this.model;
            assert(document != null, "document is null");
            const manager = widget_managers.get(document);
            assert(manager != null, "manager is null");
            this.ipy_view = await manager.render(this.model.bundle, this.container);
        }
        else {
            this.container.append(this.ipy_view.el);
        }
        if (this.ipy_view != null) {
            this.ipy_view.trigger("displayed", this.ipy_view);
        }
    }
}
class IPyWidget extends LayoutDOM {
    constructor(attrs) {
        super(attrs);
    }
    _doc_attached() {
        const doc = this.document;
        if (!widget_managers.has(doc)) {
            const manager = new WidgetManager({
                loader: generate_require_loader(this.cdn),
            });
            widget_managers.set(doc, manager);
            manager.bk_open((data) => {
                const event = new MessageSentEvent(doc, "ipywidgets_bokeh", data);
                doc._trigger_on_change(event);
            });
            doc.on_message("ipywidgets_bokeh", (data) => {
                if (isString(data) || data instanceof ArrayBuffer) {
                    manager.bk_recv(data);
                }
                else {
                    console.error(`expected a string or ArrayBuffer, got ${typeof data}`);
                }
            });
        }
    }
}
_a = IPyWidget;
IPyWidget.__name__ = "IPyWidget";
IPyWidget.__module__ = "ipywidgets_bokeh.widget";
(() => {
    _a.prototype.default_view = IPyWidgetView;
    _a.define(({ Any, String }) => ({
        bundle: [Any],
        cdn: [String, "https://unpkg.com"],
    }));
})();
export { IPyWidget };
