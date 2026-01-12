// script.js - JavaScript 모듈. 확장자를 .js

document.write("안녕하세요");  // 화면에 출력 
        console.log("개발자 도구 console에 출력")  // 화면에 안 나옴. '개발자 도구 (F12)'='접근성 속성 검사' 열면 '콘솔'에 나옴.
        // 변수 선언
        let name = "김민준";
        name = "문지영";
        console.log(name);
        const age = 27;  // 상수
        // age = 50;  // 상수는 재할당 불가능

        let info = `이름: ${name}
나이: ${age}`;
        console.log(info);
        let a = 20 ;
        let b = "20";
        console.log(typeof a);
        console.log(typeof b);
        console.log(a == b);  // 타입을 맞춘뒤 비교
        console.log(a === b);  // 타입 다르면 false