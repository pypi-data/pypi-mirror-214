import { StyleSheetLike } from "@bokehjs/core/dom";
import { LayoutDOM, LayoutDOMView } from "@bokehjs/models/layouts/layout_dom";
import { UIElement } from "@bokehjs/models/ui/ui_element";
import * as p from "@bokehjs/core/properties";
import { ModelBundle } from "./manager";
export declare class IPyWidgetView extends LayoutDOMView {
    container: HTMLDivElement;
    model: IPyWidget;
    private rendered;
    private ipy_view;
    get child_models(): UIElement[];
    connect_signals(): void;
    protected _ipy_stylesheets(): StyleSheetLike[];
    stylesheets(): StyleSheetLike[];
    render(): void;
    has_finished(): boolean;
    _render(): Promise<void>;
}
export declare namespace IPyWidget {
    type Attrs = p.AttrsOf<Props>;
    type Props = LayoutDOM.Props & {
        bundle: p.Property<ModelBundle>;
        cdn: p.Property<string>;
    };
}
export interface IPyWidget extends IPyWidget.Attrs {
}
export declare class IPyWidget extends LayoutDOM {
    properties: IPyWidget.Props;
    __view_type__: IPyWidgetView;
    constructor(attrs?: Partial<IPyWidget.Attrs>);
    static __name__: string;
    static __module__: string;
    protected _doc_attached(): void;
}
//# sourceMappingURL=widget.d.ts.map