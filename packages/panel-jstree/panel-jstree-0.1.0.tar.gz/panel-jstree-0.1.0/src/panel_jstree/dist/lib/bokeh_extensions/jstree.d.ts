import * as p from "@bokehjs/core/properties";
import { HTMLBox, HTMLBoxView } from "./layout";
export declare class jsTreePlotView extends HTMLBoxView {
    model: jsTreePlot;
    protected _container: HTMLDivElement;
    protected _id: any;
    protected _jstree: any;
    protected _last_selected: string[];
    initialize(): void;
    connect_signals(): void;
    render(): void;
    init_callbacks(): void;
    _update_code_from_editor({}: {}, data: any): void;
    _update_selection_from_value(): void;
    _update_tree_from_new_nodes(): void;
    _update_tree_from_data(): void;
    _setShowIcons(): void;
    _setShowDots(): void;
    _setMultiple(): void;
    _update_tree_theme_from_model(): void;
    _listen_for_node_open({}: {}, data: any): void;
}
export declare namespace jsTreePlot {
    type Attrs = p.AttrsOf<Props>;
    type Props = HTMLBox.Props & {
        data: p.Property<any>;
        plugins: p.Property<any>;
        multiple: p.Property<boolean>;
        show_icons: p.Property<boolean>;
        show_dots: p.Property<boolean>;
        value: p.Property<any>;
        _last_opened: p.Property<any>;
        _new_nodes: p.Property<any>;
        _flat_tree: p.Property<any>;
    };
}
export interface jsTreePlot extends jsTreePlot.Attrs {
}
export declare class jsTreePlot extends HTMLBox {
    properties: jsTreePlot.Props;
    constructor(attrs?: Partial<jsTreePlot.Attrs>);
    static __module__: string;
}
