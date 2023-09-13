import React from "react";
import AboutUsSection from "./Sections/AboutUsSection";
import SubheadingDivider from "Components/SubheadingDivider/SubheadingDivider";
import CarouselGallery from "Components/Carousel/CarouselGallery";
import LocationPage from "Containers/LocationPage/LocationPage";
import DeliverySection from "./Sections/DeliverySection";
import GallerySection from "./Sections/GallerySection";
import FlavoursAndServings from "Containers/FlavoursAndServings/FlavoursAndServings";

const HomePage = () => {
  return (
    <>
      <CarouselGallery />
      <GallerySection />
      {/* <SubheadingDivider subheadingText="Cakes for all occasions" /> */}
      <AboutUsSection />
      <FlavoursAndServings />
      <DeliverySection />
      <LocationPage />
    </>
  );
};

export default HomePage;
