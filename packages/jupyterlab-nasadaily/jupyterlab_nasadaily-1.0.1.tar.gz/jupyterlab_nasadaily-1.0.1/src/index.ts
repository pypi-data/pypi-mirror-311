import {
  ILayoutRestorer,
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import {
  ICommandPalette,
  MainAreaWidget,
  WidgetTracker,
  ToolbarButton
} from '@jupyterlab/apputils';

import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { ILauncher } from '@jupyterlab/launcher';
import { Widget } from '@lumino/widgets';
import { ISignal, Signal } from '@lumino/signaling';
import {
  refreshIcon,
  caretLeftIcon,
  caretRightIcon,
  LabIcon
} from '@jupyterlab/ui-components';

const astronautIcon = new LabIcon({
  name: 'jupyterlab_nasadaily:rocket-icon',
  // 这里填入 Font Awesome 图标的 SVG 字符串
  svgstr:
    '<svg xmlns="http://www.w3.org/2000/svg" height="16" width="16" viewBox="0 0 512 512"><!--!Font Awesome Free 6.5.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2023 Fonticons, Inc.--><path fill="navy" d="M156.6 384.9L125.7 354c-8.5-8.5-11.5-20.8-7.7-32.2c3-8.9 7-20.5 11.8-33.8L24 288c-8.6 0-16.6-4.6-20.9-12.1s-4.2-16.7 .2-24.1l52.5-88.5c13-21.9 36.5-35.3 61.9-35.3l82.3 0c2.4-4 4.8-7.7 7.2-11.3C289.1-4.1 411.1-8.1 483.9 5.3c11.6 2.1 20.6 11.2 22.8 22.8c13.4 72.9 9.3 194.8-111.4 276.7c-3.5 2.4-7.3 4.8-11.3 7.2v82.3c0 25.4-13.4 49-35.3 61.9l-88.5 52.5c-7.4 4.4-16.6 4.5-24.1 .2s-12.1-12.2-12.1-20.9V380.8c-14.1 4.9-26.4 8.9-35.7 11.9c-11.2 3.6-23.4 .5-31.8-7.8zM384 168a40 40 0 1 0 0-80 40 40 0 1 0 0 80z"/></svg>'
});

const sunIcon = new LabIcon({
  name: 'jupyterlab_nasadaily:sun-icon',
  svgstr:
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><!--!Font Awesome Free 6.7.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><g transform="scale(0.8, 0.8) translate(64, 64)"><path d="M361.5 1.2c5 2.1 8.6 6.6 9.6 11.9L391 121l107.9 19.8c5.3 1 9.8 4.6 11.9 9.6s1.5 10.7-1.6 15.2L446.9 256l62.3 90.3c3.1 4.5 3.7 10.2 1.6 15.2s-6.6 8.6-11.9 9.6L391 391 371.1 498.9c-1 5.3-4.6 9.8-9.6 11.9s-10.7 1.5-15.2-1.6L256 446.9l-90.3 62.3c-4.5 3.1-10.2 3.7-15.2 1.6s-8.6-6.6-9.6-11.9L121 391 13.1 371.1c-5.3-1-9.8-4.6-11.9-9.6s-1.5-10.7 1.6-15.2L65.1 256 2.8 165.7c-3.1-4.5-3.7-10.2-1.6-15.2s6.6-8.6 11.9-9.6L121 121 140.9 13.1c1-5.3 4.6-9.8 9.6-11.9s10.7-1.5 15.2 1.6L256 65.1 346.3 2.8c4.5-3.1 10.2-3.7 15.2-1.6zM160 256a96 96 0 1 1 192 0 96 96 0 1 1 -192 0zm224 0a128 128 0 1 0 -256 0 128 128 0 1 0 256 0z"/></g></svg>'
});

interface ICount {
  clickCount: number;
}
const BUTTON_WIDGET_CLASS = 'jp-button-widget';
class CountButtonWidget extends Widget {
  constructor(options = { node: document.createElement('button') }) {
    super(options);

    this.addClass(BUTTON_WIDGET_CLASS);

    // 创建旋转图标
    this.spinner = document.createElement('div');
    this.spinner.className = 'fa fa-sync-alt'; //fa-solid fa-arrows-rotate fa-rotate
    this.spinner.style.display = '';
    // 将旋转图标作为按钮的子元素
    this.node.appendChild(this.spinner);

    // this.node.textContent = 'Refresh';

    this.node.addEventListener('click', () => {
      this._count.clickCount = this._count.clickCount + 1;
      this._stateChanged.emit(this._count);
    });
  }

  public spinner: HTMLDivElement;

  private _count: ICount = {
    clickCount: 0
  };

  private _stateChanged = new Signal<CountButtonWidget, ICount>(this);

  public get stateChanged(): ISignal<CountButtonWidget, ICount> {
    return this._stateChanged;
  }
}

// Create ToolbarDateInput widget
class ToolbarDateInput extends Widget {
  constructor(onEnter: (dateStr: string) => void) {
    super({ node: document.createElement('input') });
    this.addClass('jp-Toolbar-dateInput');
    const input = this.node as HTMLInputElement;
    input.placeholder = 'Enter Date: YYMMDD';
    input.addEventListener('keydown', (event: KeyboardEvent) => {
      if (event.key === 'Enter') {
        onEnter(input.value);
        input.value = '';
      }
    });
  }
}

interface INASAResponse {
  copyright: string;
  date: string;
  explanation: string;
  media_type: 'video' | 'image';
  title: string;
  url: string;
  hdurl: string;
}

class NASAWidget extends Widget {
  // The image element associated with the widget.
  readonly imageContainer: HTMLDivElement;
  readonly img: HTMLImageElement;
  // The imgtitle text element associated with the widget.
  readonly imgtitle: HTMLParagraphElement;
  readonly copyright: HTMLParagraphElement;
  // 定义 icon 元素
  readonly spinner: HTMLDivElement;

  readonly refreshbutton: CountButtonWidget;
  // API key for the NASA API
  private apiKey: string;
  private minDate: Date;
  private useOpenAI: boolean;
  private openaiKey: string;
  private openaiModel: string;
  private prompt: string;

  // Add currentDate property
  public currentDate: Date;

  // Add a controller to manage fetchMoreExplanation requests
  private fetchController: AbortController | null = null;

  /**
   * Construct a new NASA widget.
   */
  constructor(userSettings: ISettingRegistry.ISettings | null) {
    super();

    this.addClass('nasa-widget');

    this.apiKey = (userSettings?.composite['api_key'] as string) || 'DEMO_KEY';
    this.useOpenAI = (userSettings?.composite['use_openai'] as boolean) ?? true;
    this.openaiKey =
      (userSettings?.composite['openai_key'] as string) || 'None';
    this.openaiModel =
      (userSettings?.composite['openai_model'] as string) || 'gpt-4o-mini';
    this.prompt =
      (userSettings?.composite['prompt'] as string) ||
      "This is the description of an image from NASA's Astronomy Picture of the Day. Elaborate more on relevant scientific discoveries, theories, narratives, or anecdotes behind the image and its description. Explain any technical or professional terms and names in simple language for better understanding. Generate an HTML snippet using only the simplest formatting elements, such as <b> for bold, <i> for italics, <p> for paragraphs, and <br> for line breaks. Avoid including any styles, colors, fonts, or size adjustments. Keep the structure clean and minimal.";

    const minDateStr =
      (userSettings?.composite['min_date'] as string) || '1995-07-01';
    this.minDate = isNaN(Date.parse(minDateStr))
      ? new Date('1995-07-01')
      : new Date(minDateStr);

    this.refreshbutton = new CountButtonWidget();
    // this.addWidget(this._button);
    this.node.appendChild(this.refreshbutton.node);
    this.refreshbutton.stateChanged.connect(this._onRefresh, this);

    // 创建包裹容器
    this.imageContainer = document.createElement('div');
    this.imageContainer.className = 'image-container'; // 设置类名以便样式化

    // 添加图片元素到包裹容器
    this.img = document.createElement('img');
    this.imageContainer.appendChild(this.img);

    // 添加摘要元素到面板
    this.imgtitle = document.createElement('p');
    this.imgtitle.className = 'nasa-imgtitle'; // 为摘要元素设置一个类名
    this.node.appendChild(this.imgtitle);

    // 添加版权信息到面板
    this.copyright = document.createElement('p');
    this.copyright.className = 'nasa-copyright'; // 为版权信息设置一个类名
    this.imageContainer.appendChild(this.copyright);

    // 创建并添加旋转图标
    this.spinner = document.createElement('div');
    this.spinner.className = 'fa fa-spinner fa-spin'; // 使用 Font Awesome 的旋转图标
    // this.spinner.className = 'fa fa-rocket fa-spin'
    this.spinner.style.display = 'none'; // 默认隐藏
    this.node.appendChild(this.spinner);

    this.node.appendChild(this.imageContainer);

    // 为图片添加加载完成的监听器
    this.img.onload = () => {
      // 图片加载完成后的操作
      this.onImageLoaded();
    };

    // Initialize currentDate
    this.currentDate = new Date();
  }

  // Add formatDate method
  public formatDate(date: Date): string {
    return date.toISOString().slice(0, 10);
  }

  private _onRefresh(emitter: CountButtonWidget, count: ICount): void {
    this.updateNASAImage(undefined, true);
    console.log('Hey, a Signal has been received from', emitter);
    console.log(`Image refreshed ${count.clickCount} times.`);
  }

  // 图片加载完成后的处理函数
  private onImageLoaded(): void {
    // 隐藏旋转图标
    this.refreshbutton.spinner.className = 'fa fa-sync-alt';
    this.spinner.style.display = 'none';

    // 显示图片和摘要
    this.img.style.display = '';
    this.imgtitle.style.display = '';
    this.copyright.style.display = '';
  }

  /**
   * Handle update requests for the widget.
   */
  async updateNASAImage(
    date?: string,
    isRandom: boolean = false
  ): Promise<void> {
    // If date is provided, use it; else generate random date
    let fetchDate: string;
    if (date) {
      fetchDate = date;
      this.currentDate = new Date(date);
    } else if (isRandom) {
      fetchDate = this.randomDate();
      this.currentDate = new Date(fetchDate);
    } else {
      fetchDate = this.formatDate(new Date()); // Use today's date
      this.currentDate = new Date(fetchDate);
    }

    // Use DEMO_KEY if no API key is provided
    const response = await fetch(
      `https://api.nasa.gov/planetary/apod?api_key=${
        this.apiKey
      }&date=${fetchDate}`
    );
    // 显示旋转图标
    this.refreshbutton.spinner.className = 'fa fa-sync-alt fa-spin'; // 开始旋转
    this.spinner.style.display = '';

    // 隐藏图片和摘要，以防止显示旧内容
    this.img.style.display = 'none';
    this.imgtitle.style.display = 'none';
    this.copyright.style.display = 'none';
    let moreExplanation = '';

    //清空html内容
    this.imgtitle.innerHTML = '';
    this.copyright.innerHTML = '';

    if (!response.ok) {
      const data = await response.json();
      if (data.code === 404) {
        // If data not available for current date, try previous day
        const prevDate = new Date(this.currentDate);
        prevDate.setDate(prevDate.getDate() - 1);
        this.currentDate = prevDate;
        await this.updateNASAImage(this.formatDate(prevDate), isRandom);
        return;
      }
      if (data.error) {
        this.imgtitle.innerText = data.error.message;
      } else {
        this.imgtitle.innerText = response.statusText;
      }
      // 隐藏旋转图标
      this.refreshbutton.spinner.className = 'fa fa-sync-alt';
      this.spinner.style.display = 'none';
      this.imgtitle.style.display = '';
      return;
    }

    const data = (await response.json()) as INASAResponse;

    if (data.media_type === 'image') {
      // Populate the image
      this.img.src = data.url;
      // this.img.title = data.title;
      this.imgtitle.innerText = data.title;
      // 如果copyright或explainnation一个不为空，则显示
      // 去掉换行符
      if (
        data.date ||
        data.copyright ||
        data.explanation ||
        data.url ||
        data.hdurl
      ) {
        const page_url = `https://apod.nasa.gov/apod/ap${this.transformDate(data.date)}.html`;
        this.copyright.innerHTML = `
        <span style="color: cyan; font-weight: bold;">${data.date || ''}</span> : 
        ${data.explanation || ''}<br>
        <em>Copyright: ${data.copyright || 'NASA'} || 
        <a href="${page_url}" target="_blank">Page Link</a> || 
        <a href="${data.url}" target="_blank">Image Link</a> || 
        <a href="${data.hdurl}" target="_blank">HD Image Link</a></em>
        `.replace(/[\r\n]/g, '');
        // Cancel the previous fetchMoreExplanation request if it exists
        if (this.fetchController) {
          this.fetchController.abort();
        }
        // Create a new AbortController for the current request
        this.fetchController = new AbortController();
        moreExplanation = await this.fetchMoreExplanation(
          data,
          this.fetchController.signal
        );

        this.copyright.innerHTML = `
        <span style="color: cyan; font-weight: bold;">${data.date || ''}</span> : 
        ${data.explanation || ''}<br>
        ${moreExplanation ? '<hr>' + moreExplanation + '<hr>' : ''}
        <em>Copyright: ${data.copyright || 'NASA'} ||
        <a href="${page_url}" target="_blank">Page Link</a> || 
        <a href="${data.url}" target="_blank">Image Link</a> || 
        <a href="${data.hdurl}" target="_blank">HD Image Link</a></em>
        `.replace(/[\r\n]/g, '');
      }
    } else if (data.media_type === 'video') {
      console.log('This is a video. Click link to view.');
      const page_url = `https://apod.nasa.gov/apod/ap${this.transformDate(data.date)}.html`;
      this.imgtitle.innerHTML = `
        <span style="color: cyan; font-weight: bold;">${data.date || ''}</span> :
        <span style="color: skyblue; font-weight: bold;">${data.title || ''}</span> || 
        <a href="${page_url}" target="_blank" style="color: blue; font-weight: bold;">Page Link</a> || 
        <a href="${data.url}" target="_blank" style="color: blue; font-weight: bold;">Video Link</a> <br>
        ${data.explanation || ''}<br>
        `.replace(/[\r\n]/g, '');
      // Cancel the previous fetchMoreExplanation request if it exists
      if (this.fetchController) {
        this.fetchController.abort();
      }
      // Create a new AbortController for the current request
      this.fetchController = new AbortController();
      moreExplanation = await this.fetchMoreExplanation(
        data,
        this.fetchController.signal
      );
      this.imgtitle.innerHTML = `
        <span style="color: cyan; font-weight: bold;">${data.date || ''}</span> :
        <span style="color: skyblue; font-weight: bold;">${data.title || ''}</span> || 
        <a href="${page_url}" target="_blank" style="color: blue; font-weight: bold;">Page Link</a> || 
        <a href="${data.url}" target="_blank" style="color: blue; font-weight: bold;">Video Link</a> <br>
        ${data.explanation || ''}<br>
        ${moreExplanation ? '<hr>' + moreExplanation + '<hr>' : ''}
        `.replace(/[\r\n]/g, '');
      this.refreshbutton.spinner.className = 'fa fa-sync-alt';
      this.spinner.style.display = 'none';
      this.imgtitle.style.display = '';
    } else {
      this.imgtitle.innerText =
        'This random fetch is not an image. Please refresh again.';
      // 隐藏旋转图标
      this.refreshbutton.spinner.className = 'fa fa-sync-alt';
      this.spinner.style.display = 'none';
      this.imgtitle.style.display = '';
    }
  }

  /**
   * Get a random date string in YYYY-MM-DD format.
   */
  randomDate(): string {
    const start = this.minDate;
    const end = new Date();
    const randomDate = new Date(
      start.getTime() + Math.random() * (end.getTime() - start.getTime())
    );
    return randomDate.toISOString().slice(0, 10);
  }

  // Implement handleDateInput
  public handleDateInput(dateStr: string): void {
    const extractedDateStr = this.extractDate(dateStr);
    let date: Date;
    if (extractedDateStr) {
      date = new Date(extractedDateStr);
    } else {
      date = new Date();
    }
    const today = new Date();
    if (date > today) {
      date = today;
    }
    if (date < this.minDate) {
      date = this.minDate;
    }
    this.updateNASAImage(this.formatDate(date));
  }

  // Implement extractDate
  private extractDate(input: string): string | null {
    const patterns = [
      /^(\d{4})(\d{2})(\d{2})$/, // YYYYMMDD
      /^(\d{2})(\d{2})(\d{2})$/, // YYMMDD
      /^(\d{4})-(\d{2})-(\d{2})$/ // YYYY-MM-DD
    ];
    for (const pattern of patterns) {
      const match = input.match(pattern);
      if (match) {
        let year = match[1];
        const month = match[2];
        const day = match[3];
        if (year.length === 2) {
          // Assume 19xx for years >= 90 and 20xx for years < 70
          year = parseInt(year, 10) >= 90 ? '19' + year : '20' + year;
        }
        return `${year}-${month}-${day}`;
      }
    }
    return null;
  }

  // Transform date string from YYYY-MM-DD to YYMMDD
  private transformDate(dateStr: string): string {
    return dateStr.slice(2).replace(/-/g, '');
  }

  // Implement fetchMoreExplanation
  private async fetchMoreExplanation(
    data: INASAResponse,
    signal: AbortSignal
  ): Promise<string> {
    let moreExplanation = '';
    if (this.useOpenAI && this.openaiKey !== 'None') {
      try {
        const openaiResponse = await fetch(
          'https://api.openai.com/v1/chat/completions',
          {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              Authorization: `Bearer ${this.openaiKey}`
            },
            body: JSON.stringify({
              model: this.openaiModel,
              messages: [
                {
                  role: 'user',
                  content: `${this.prompt}\n\n------\nTitle: ${data.title} || ${data.date}\nDescription: ${data.explanation}\n------\n`
                }
              ]
            }),
            signal: signal
          }
        );

        if (!openaiResponse.ok) {
          console.error('OpenAI API error:', openaiResponse.statusText);
          return '';
        }

        const openaiData = await openaiResponse.json();

        if (
          openaiData &&
          openaiData.choices &&
          openaiData.choices.length > 0 &&
          openaiData.choices[0].message &&
          openaiData.choices[0].message.content
        ) {
          // 如果explanation中有```html ... ```则提取其中的内容
          const htmlPattern = /```html([\s\S]*?)```/g;
          const matches =
            openaiData.choices[0].message.content.match(htmlPattern);
          if (matches) {
            for (const match of matches) {
              moreExplanation += match
                .replace(/```html/g, '')
                .replace(/```/g, '');
            }
          } else {
            moreExplanation = openaiData.choices[0].message.content;
          }
        } else {
          console.error('Invalid OpenAI response format:', openaiData);
        }
      } catch (error) {
        if ((error as Error).name === 'AbortError') {
          console.log('Fetch aborted');
        } else {
          console.error('Error fetching from OpenAI:', error);
        }
      }
    } else {
      console.log(
        'OpenAI elaboration is disabled or OpenAI API key not provided.'
      );
    }

    return moreExplanation;
  }
}

/**
 * Activate the NASA widget extension.
 */
function activate(
  app: JupyterFrontEnd,
  palette: ICommandPalette,
  settingRegistry: ISettingRegistry | null,
  restorer: ILayoutRestorer | null,
  launcher: ILauncher | null
) {
  console.log('JupyterLab extension jupyterlab_nasadaily:plugin is activated!');

  // Declare a widget variable
  let widget: MainAreaWidget<NASAWidget>;
  let mysettings: ISettingRegistry.ISettings;

  //console.log(settingRegistry?.load('jupyterlab_nasadaily:plugin'))
  // Load settings
  if (settingRegistry) {
    settingRegistry
      .load('jupyterlab_nasadaily:plugin')
      .then(settings => {
        mysettings = settings;
      })
      .catch(reason => {
        console.error(
          'failed to load settings for jupyterlab_nasadaily:plugin.',
          reason
        );
      });
  }

  // Add an application command
  const command: string = 'nasa:open';
  app.commands.addCommand(command, {
    label: 'NASA Daily',
    execute: () => {
      if (!widget || widget.isDisposed) {
        const content = new NASAWidget(mysettings);
        widget = new MainAreaWidget({ content });
        widget.id = 'nasa-pic';
        widget.title.label = 'NASA Daily';
        widget.title.icon = astronautIcon; // imageIcon
        widget.title.closable = true;
      }
      if (!tracker.has(widget)) {
        // Track the state of the widget for later restoration
        tracker.add(widget);
      }
      if (!widget.isAttached) {
        // Attach the widget to the main work area if it's not there
        app.shell.add(widget, 'main');
      }
      widget.content.updateNASAImage();

      // Add 'Today' button
      const todayButton = new ToolbarButton({
        label: 'Today',
        icon: sunIcon,
        onClick: () => {
          const today = new Date();
          widget.content.updateNASAImage(widget.content.formatDate(today));
        }
      });
      widget.toolbar.addItem('today', todayButton);

      // Add 'Previous Day' button
      const prevButton = new ToolbarButton({
        label: 'Prev Day',
        icon: caretLeftIcon,
        onClick: () => {
          widget.content.currentDate.setDate(
            widget.content.currentDate.getDate() - 1
          );
          widget.content.updateNASAImage(
            widget.content.formatDate(widget.content.currentDate)
          );
        }
      });
      widget.toolbar.addItem('previous', prevButton);

      // Add 'Next Day' button
      const nextButton = new ToolbarButton({
        label: 'Next Day',
        icon: caretRightIcon,
        onClick: () => {
          widget.content.currentDate.setDate(
            widget.content.currentDate.getDate() + 1
          );
          widget.content.updateNASAImage(
            widget.content.formatDate(widget.content.currentDate)
          );
        }
      });
      widget.toolbar.addItem('next', nextButton);

      // Add refresh button
      const refreshButton = new ToolbarButton({
        label: 'Random Day',
        icon: refreshIcon,
        onClick: () => widget.content.updateNASAImage(undefined, true)
      });
      widget.toolbar.addItem('refresh', refreshButton);

      // Add date input widget
      const dateInput = new ToolbarDateInput((dateStr: string) => {
        widget.content.handleDateInput(dateStr);
      });
      widget.toolbar.addItem('dateInput', dateInput);

      // Activate the widget
      app.shell.activateById(widget.id);
    },
    icon: astronautIcon // imageIcon
  });

  // Add the command to the palette.
  palette.addItem({ command, category: 'NASA' });

  // Track and restore the widget state
  const tracker = new WidgetTracker<MainAreaWidget<NASAWidget>>({
    namespace: 'nasa'
  });
  // Track and restore the widget state
  if (restorer) {
    restorer.restore(tracker, {
      command,
      name: () => 'nasa'
    });
  }

  // Add to launcher
  if (launcher) {
    launcher.add({ command, category: 'Other', rank: 1 });
  }
}

/**
 * Initialization data for the jupyterlab_nasadaily extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'jupyterlab_nasadaily:plugin',
  description:
    'JupyterLab Extension to Show Astronomy Picture of the Day from NASA',
  autoStart: true,
  requires: [ICommandPalette, ISettingRegistry],
  optional: [ILayoutRestorer, ILauncher],
  activate: activate
};

export default plugin;
