import { Observable } from 'rxjs';

export interface CrawlList {
  date: string;
  value: number;
  delta: {
    up: boolean;
    value: number;
  };
  comparison: {
    prevDate: string;
    prevValue: number;
    nextDate: string;
    nextValue: number;
  };
}

export abstract class CrawlListData {
  abstract getCrawlListData(period: string): Observable<CrawlList>;
}